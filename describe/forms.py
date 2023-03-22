from crispy_forms.helper import FormHelper
from django import forms
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseInlineFormSet
from django.urls import reverse_lazy
from django.utils.html import format_html
from dynamic_forms import DynamicField, DynamicFormMixin
from numpy import obj2sctype

from register.models import PlantVariety

from .models import Description, Protocol, Trait, State


class TraitForm(forms.Form):
    numeric_id = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    protocol_id = forms.IntegerField(widget=forms.HiddenInput)


StateFormset = inlineformset_factory(
    Trait,
    State,
    extra=1,
    fields=(
        "numeric_id",
        "description",
    ),
)


class BaseTraitFormSet(BaseInlineFormSet):
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
    fields=(
        "numeric_id",
        "description",
        "grouping",
    ),
)


class ExpressionForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    state = forms.ModelChoiceField(queryset=State.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpressionForm, self).__init__(*args, **kwargs)
        self.fields["state"].required = False
        self.fields["id"].required = False


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
            self.fields["state"].label = format_html(
                f"<b>{trait.numeric_id}. {trait.description}</b>"
            )
        else:
            self.fields["state"].label = format_html(
                f"{trait.numeric_id}. {trait.description}"
            )


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


DescriptionFilterFormSet = formset_factory(
    DescriptionFilterForm, formset=BaseDescriptionFilterFormset, extra=0
)


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())


def _choices(form, model, depends_on):
    value = form[depends_on].value()
    if value:
        return model.objects.filter(**{depends_on: value})
    else:
        return model.objects.none()


class RelatedStateForm(DynamicFormMixin, forms.Form):
    def protocol_choices(form):
        state = form["state"].value()
        state = State.objects.get(pk=state)
        protocol = state.trait.protocol
        return Protocol.objects.filter(plantspecies=protocol.plantspecies).exclude(
            pk=protocol.pk
        )

    state = forms.IntegerField(widget=forms.HiddenInput())

    protocol = DynamicField(
        forms.ModelChoiceField,
        queryset=protocol_choices,
    )
    trait = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: _choices(form, Trait, "protocol"),
    )
    related_state = DynamicField(
        forms.ModelChoiceField, queryset=lambda form: _choices(form, State, "trait")
    )


class DescriptionForm(forms.Form):
    VARIETY_CHOICES = [("", "--------"),] + [
        (variety["pk"], f"{variety['name']} ({variety['species__latin_name']})")
        for variety in PlantVariety.objects.values("pk", "name", "species__latin_name")
    ]
    variety = forms.ChoiceField(
        choices=VARIETY_CHOICES, required=True, label="Variety", label_suffix=""
    )
    protocol = forms.CharField(label="Protocol", label_suffix="")
    name = forms.CharField(label="Source", label_suffix="")

    def save(self):
        data = self.cleaned_data
        variety = PlantVariety.objects.get(pk=data["variety"])
        protocol = Protocol.objects.get(pk=data["protocol"])
        description = Description(variety=variety, protocol=protocol, name=data["name"])
        description.save()
        return description
