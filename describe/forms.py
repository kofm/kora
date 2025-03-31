from typing import Any

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.db.models import QuerySet
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.urls import reverse
from dynamic_forms import DynamicField, DynamicFormMixin

from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
)
from register.models import PlantVariety


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


class DescriptionNameForm(forms.Form):
    name = forms.MultipleChoiceField(
        choices=[("", "")] + Description.names(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )


class DescriptionVarietyForm(forms.Form):
    variety = forms.CharField(widget=DescriptorTextInput(), required=False)


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(
        queryset=Protocol.objects.select_related("plantspecies").all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": "Select Protocol",
            }
        ),
    )


class ProtocolStrictSearchForm(forms.Form):
    strict = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )


def _choices(form, model, depends_on):
    value = form[depends_on].value()
    if value:
        return model.objects.filter(**{depends_on: value})
    else:
        return model.objects.none()


class ProtocolMetadataForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ("name", "url_ref", "order")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "url_ref": forms.URLInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class RelatedStateForm(DynamicFormMixin, forms.Form):
    def protocol_choices(self, form):
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

    variety = forms.ModelChoiceField(queryset=PlantVariety.objects.select_related("species").all())

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
        super().__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs) -> None:
        trait = kwargs.pop("trait", None)
        super().__init__(*args, **kwargs)
        self.auto_id = False
        if trait:
            self.fields["state"].queryset = State.objects.filter(trait=trait)  # type: ignore[attr-defined]


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
                css_class="form-select",
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
        script = f"""
        on click from elsewhere wait 100ms then fetch
        {reverse("describe:workspace_detail")} then put the result
        into #workspaceBody then call htmx.process(#workspaceBody)
        """
        self.helper.layout = Layout(
            FieldWithButtons(
                Field("name", script=script),
                StrictButton(
                    "<i class='bi bi-check'></i>",
                    css_class="btn btn-outline-success",
                    type="submit",
                ),
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


class ExpressionFilterForm(forms.Form):
    trait = forms.IntegerField(widget=forms.HiddenInput())
    expressions = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        state_choices = kwargs.pop("state_choices", [])
        trait_description = kwargs.pop("trait", [])
        super().__init__(*args, **kwargs)
        self.fields["expressions"].label = trait_description
        self.fields["expressions"].choices = state_choices


class BaseExpressionFilterFormSet(BaseFormSet):
    """Provides the UI for filtering Descriptions by Expression.

    Args:

        traits (QuerySet): a Trait QuerySet, ideally returned from
        `get_protocol_traits()`

        expressions (dict, optional): a dict[str, list] of expressions

    """

    def __init__(self, *args, traits: Any, **kwargs):
        self.traits: QuerySet[Trait] = traits
        self.expressions: dict[str, list] = kwargs.pop("expressions", {})
        super().__init__(*args, **kwargs)
        self.initial = self._get_initial_data()

    def _get_initial_data(self):
        initial = []
        for trait in self.traits:
            initial.append({"trait": trait.pk, "expressions": self.expressions.get(str(trait.pk), [])})
        return initial

    def _render_choices(self, state: State):
        return (state.pk, f" {state.numeric_id}. {state.description}")

    def _render_label(self, trait: Trait):
        return f"{trait.numeric_id}. {trait.description}"

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        if self.traits and index < len(self.traits):
            trait = self.traits[index]
            kwargs["state_choices"] = [self._render_choices(state) for state in trait.states.all()]
            kwargs["trait"] = self._render_label(trait)
        return kwargs

    def get_expression_ids(self) -> dict:
        """Returns a list of Expression ids to be used with
        `Description.objects.filtery_by_expressions()`
        """
        return {
            form.cleaned_data["trait"]: form.cleaned_data["expressions"]
            for form in self
            if form.is_valid() and form.cleaned_data.get("expressions")
        }


ExpressionFilterFormSet = formset_factory(ExpressionFilterForm, formset=BaseExpressionFilterFormSet, extra=0)
