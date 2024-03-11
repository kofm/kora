from django.core.validators import MaxLengthValidator
from dynamic_forms import DynamicField, DynamicFormMixin

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html

from .models import Description, Expression, Protocol, State, Trait


class TraitForm(forms.Form):
    numeric_id = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    protocol_id = forms.IntegerField(widget=forms.HiddenInput)


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = (
            "numeric_id",
            "description",
        )
        labels = {
            "numeric_id": "Note N°",
            "description": "Note description",
        }


StateFormset = inlineformset_factory(
    Trait,
    State,
    form=StateForm,
    extra=1,
    fields=(
        "numeric_id",
        "description",
    ),
)


class BaseTraitFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_labels = {}
        self.custom_labels["numeric_id"] = "Characteristic N°"
        self.custom_labels["description"] = "Characteristic description"
        for form in self.forms:
            form.fields["numeric_id"].label = self.custom_labels["numeric_id"]
            form.fields["description"].label = self.custom_labels["description"]

    def add_fields(self, form, index):
        form.nested = StateFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix="state-%s-%s" % (form.prefix, StateFormset.get_default_prefix()),
        )
        return super().add_fields(form, index)

    def is_valid(self):
        result = super(BaseTraitFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def empty_form(self):
        form = super().empty_form
        form.fields["numeric_id"].label = self.custom_labels["numeric_id"]
        form.fields["description"].label = self.custom_labels["description"]
        return form

    def save(self, commit=True):
        result = super(BaseTraitFormSet, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


TraitFormSet = inlineformset_factory(
    Protocol,
    Trait,
    formset=BaseTraitFormSet,
    extra=1,
    fields=("numeric_id", "description", "grouping"),
)


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
    state = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super(DescriptionFilterForm, self).__init__(*args, **kwargs)
        trait = Trait.objects.get(pk=self.initial["trait"])
        self.fields["state"].queryset = State.objects.filter(trait=trait)
        # self.fields["state"].label = format_html(str(trait.numeric_id) + ". " + trait.description)
        if trait.grouping:
            self.fields["state"].label = format_html(f"<b>{trait.numeric_id}. {trait.description}</b>")
        else:
            self.fields["state"].label = format_html(f"{trait.numeric_id}. {trait.description}")


class BaseDescriptionFilterFormset(BaseFormSet):
    def save(self):
        filter = list()
        for form in self.forms:
            if states := form.cleaned_data["state"]:
                filter.append(
                    {
                        "trait": form.cleaned_data["trait"],
                        "state": [state.pk for state in states],
                    }
                )
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


class ProtocolNameForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ("name",)


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
