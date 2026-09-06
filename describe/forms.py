from typing import Any

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.db.models import QuerySet
from django.forms import BaseInlineFormSet, ModelChoiceField, formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html

from describe.models import (
    Description,
    DescriptionLabel,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
)
from frontpage.forms import TomSelectModelFormMixin
from frontpage.widgets import (
    BootstrapNumberInput,
    BootstrapTextInput,
    LabelColourSelect,
    LabelSelect,
    LabelSelectMultiple,
    ModelTomSelect,
    TomSelect,
    TomSelectConfig,
)
from register.models import PlantSpecies, PlantVariety


class TraitForm(forms.ModelForm):
    class Meta:
        model = Trait
        fields = ("numeric_id", "description", "grouping", "protocol")
        widgets = {
            "numeric_id": BootstrapNumberInput(attrs={"placeholder": "ID"}),
            "description": BootstrapTextInput(
                attrs={
                    "placeholder": "Description",
                    "aria-describedby": "descriptorHelp",
                }
            ),
            "grouping": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "protocol": forms.HiddenInput,
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ("id", "numeric_id", "description", "trait")
        widgets = {
            "numeric_id": BootstrapNumberInput(attrs={"placeholder": "ID"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "trait": forms.HiddenInput(),
        }


class BaseInlineStateFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        """A new State must be created in a singleton group"""
        form.instance.reset_group()
        return super().save_new(form, commit=commit)


StateFormSet = inlineformset_factory(
    Trait,
    State,
    form=StateForm,
    formset=BaseInlineStateFormSet,
    extra=1,
    can_delete=False,
    can_order=False,
)


class ExpressionUpdateForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False)
    note = forms.CharField(required=False)


class DescriptionLabelsForm(forms.Form):
    labels = forms.ModelMultipleChoiceField(
        label="Label",
        widget=LabelSelectMultiple(),
        queryset=DescriptionLabel.objects.all(),
        required=False,
    )


class DescriptionVarietyForm(forms.Form):
    variety = forms.CharField(widget=BootstrapTextInput(), required=False)


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(
        queryset=Protocol.objects.select_related("plantspecies").all(),
        widget=TomSelect(attrs={"aria-label": "Select Protocol"}),
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


class TomSelectModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # We sync the Form label with tomselect rendering for when initial values are set
        label_field = self.widget.ts_config.options.get("label_field")
        if label_field:
            return str(getattr(obj, label_field))
        return str(obj)


class DescriptionForm(TomSelectModelFormMixin, forms.ModelForm):
    """Form used to create or update a Description."""

    species = TomSelectModelChoiceField(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
    )
    variety = TomSelectModelChoiceField(
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            ),
        ),
    )

    protocol = ModelChoiceField(
        queryset=Protocol.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:protocol_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="plantspecies_id",
            ),
        ),
    )
    label = ModelChoiceField(queryset=DescriptionLabel.objects.all(), widget=LabelSelect(), required=False)

    class Meta:
        model = Description
        fields = ("species", "variety", "protocol", "label")


class DescriptionDuplicateForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ("label",)
        widgets = {"name": LabelSelect()}


class DescriptionUpdateForm(forms.ModelForm):
    label = forms.ModelChoiceField(queryset=DescriptionLabel.objects.all(), widget=LabelSelect())
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Description
        fields = ("label", "notes")


class ExpressionForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.none(), blank=False)

    class Meta:
        model = Expression
        fields = ("description", "state", "note")
        widgets = {
            "description": forms.HiddenInput(),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Notes:"}),
        }


class WorkspaceSelectForm(forms.Form):
    workspace = forms.ModelChoiceField(queryset=Workspace.objects.none(), label="Active Workspace", required=False)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.user = user
        workspaces = Workspace.objects.filter(user=self.user)
        self.fields["workspace"].queryset = workspaces
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field(
                "workspace",
                css_class="form-select",
                hx_post=reverse("describe:workspace_activate"),
                hx_trigger="change",
                hx_target="#workspaceBody",
            )
        )

    def save(self):
        workspace = self.cleaned_data.get("workspace")
        Workspace.objects.filter(user=self.user).deactivate_all()
        if workspace:
            workspace.is_active = True
            workspace.save()
        return workspace


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
    expressions = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}), required=False
    )

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
        # Grouping traits should be highlighted
        if trait.grouping:
            return format_html("<b>&#10033; {}. {}</b>", trait.numeric_id, trait.description)
        return format_html("{}. {}", trait.numeric_id, trait.description)

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


class TraitStatesForm(forms.Form):
    protocol = forms.ChoiceField(choices=[], label="")
    trait = forms.ChoiceField(choices=[], label="")


class DescriptionLabelForm(forms.ModelForm):
    class Meta:
        model = DescriptionLabel
        fields = ("name", "colour")
        widgets = {"colour": LabelColourSelect()}


class DescriptionFilterLabelForm(forms.Form):
    labels = forms.ModelMultipleChoiceField(
        queryset=DescriptionLabel.objects.all(),
        widget=LabelSelectMultiple,
    )
