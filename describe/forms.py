from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.forms import CheckboxSelectMultiple, formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.urls import reverse
from django.utils.html import format_html
from dynamic_forms import DynamicField, DynamicFormMixin

from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
)


class NumberingCodeInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {
            "class": "form-control",
            "inputmode": "numeric",
            "placeholder": "ID",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class DescriptorTextInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {"class": "form-control"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TraitForm(forms.ModelForm):
    class Meta:
        model = Trait
        fields = ("numeric_id", "description", "grouping", "protocol")
        widgets = {
            "numeric_id": NumberingCodeInput,
            "description": DescriptorTextInput(
                attrs={"placeholder": "Description", "aria-describedby": "descriptorHelp"}
            ),
            "grouping": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "protocol": forms.HiddenInput,
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ("id", "numeric_id", "description", "trait")
        widgets = {
            "numeric_id": NumberingCodeInput(),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Descriptor state"}),
            "trait": forms.HiddenInput(),
        }


StateFormSet = inlineformset_factory(Trait, State, form=StateForm, extra=1, can_delete=False, can_order=False)


class ExpressionUpdateForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False)
    note = forms.CharField(required=False)


class DescriptionFilterForm(forms.Form):
    """
    This is the single unit of the form to filter descriptions.
    It needs to be instantiated with a trait id to populate the available states of expression field.
    """

    trait = forms.IntegerField(widget=forms.HiddenInput())
    state = forms.ModelMultipleChoiceField(queryset=None, required=False, widget=CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(DescriptionFilterForm, self).__init__(*args, **kwargs)
        trait = Trait.objects.get(pk=self.initial["trait"])
        self.fields["state"].queryset = State.objects.filter(trait=trait)
        if trait.grouping:
            self.fields["state"].label = format_html(f"<b>{trait.numeric_id}. {trait.description}</b>")
        else:
            self.fields["state"].label = format_html(f"{trait.numeric_id}. {trait.description}")


class BaseDescriptionFilterFormset(BaseFormSet):
    def save(self):
        filter = list()
        for form in self.forms:
            if states := form.cleaned_data["state"]:
                filter.append({"trait": form.cleaned_data["trait"], "state": [state.pk for state in states]})
        return filter


DescriptionFilterFormSet = formset_factory(DescriptionFilterForm, formset=BaseDescriptionFilterFormset, extra=0)


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())


def _choices(form, model, depends_on):
    value = form[depends_on].value()
    if value:
        return model.objects.filter(**{depends_on: value})
    else:
        return model.objects.none()


class ProtocolMetadataForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ("name", "url_ref")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "url_ref": forms.URLInput(attrs={"class": "form-control"}),
        }


class RelatedStateForm(DynamicFormMixin, forms.Form):
    def protocol_choices(form):
        state = form["state"].value()
        state = State.objects.get(pk=state)
        protocol = state.trait.protocol
        return Protocol.objects.filter(plantspecies=protocol.plantspecies).exclude(pk=protocol.pk)

    state = forms.IntegerField(widget=forms.HiddenInput())

    protocol = DynamicField(
        forms.ModelChoiceField,
        queryset=protocol_choices,
    )
    trait = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: _choices(form, Trait, "protocol"),
    )
    related_state = DynamicField(forms.ModelChoiceField, queryset=lambda form: _choices(form, State, "trait"))


class DescriptionForm(forms.ModelForm):
    """Form used to create or update a Description."""

    def __init__(self, *args, **kwargs):
        """Initialize a DescriptionForm.

            The model field `name` is a CharField but we want the user to be
        able to select a value from a pre-populated list of values (to
        prevent duplication); therefore, in the __init__ method the `name`
        field widget is set to a `forms.Select` and the available choices
        to the unique values of the `name` field within the entire
        database. This allow keeping the correct CharField validation
        while allowing the creation of a TomSelect widget populated from
        the original <select> element. Using a ChoiceField directly would
        have automatically introduced a validation against the available
        choices, which is not what we want here since the user *can*
        create new `name` values."""
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget = forms.Select(choices=Description.names())

    class Meta:
        model = Description
        fields = ("variety", "protocol", "name")


class DescriptionUpdateForm(DescriptionForm):
    class Meta:
        model = Description
        fields = ("variety", "name")


class ExpressionForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.none(), blank=False)

    class Meta:
        model = Expression
        fields = ("description", "state", "note")
        widgets = {"description": forms.HiddenInput()}

    def __init__(self, *args, trait=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.auto_id = False
        if trait:
            self.fields["state"].queryset = State.objects.filter(trait=trait)


class WorkspaceSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Workspace.objects.none(), label="Active Workspace")

    class Meta:
        model = Workspace
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        if request.user.is_authenticated:
            self.fields["name"].queryset = Workspace.objects.filter(user=request.user)
            active_list = request.user.workspace_set.filter(is_active=True)
            if active_list.exists():
                self.fields["name"].initial = active_list.first().pk
        else:
            self.fields["name"].disabled = True
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field(
                "name",
                css_class="form-control",
                hx_post=reverse("describe:workspace_activate"),
                hx_trigger="change",
                hx_target="#workspaceBody",
            )
        )


class WorkspaceInputForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label_suffix = ""
        self.fields["name"].help_text = ""
        self.helper = FormHelper(self)
        script = f"""on click from elsewhere wait 100ms then fetch {reverse("describe:workspace_list")}
        then put the result into #workspaceBody then call htmx.process(#workspaceBody)"""
        self.helper.attrs = {"hx_post": reverse("describe:workspace_create")}
        self.helper.layout = Layout(
            FieldWithButtons(
                Field("name", script=script),
                StrictButton("<i class='bi bi-check'></i>", css_class="btn btn-outline-success", type="submit"),
            )
        )


class WorkspaceCreateForm(WorkspaceInputForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Create Workspace"
        self.helper.attrs = {"hx_post": reverse("describe:workspace_create")}


class WorkspaceUpdateForm(WorkspaceInputForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Rename Workspace"
        self.helper.attrs = {"hx_post": reverse("describe:workspace_update", args=(self.instance.pk,))}
