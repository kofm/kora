from django import forms
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.urls import reverse_lazy
from django.utils.html import format_html

from .models import Protocol, Trait, State


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


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(
        queryset=Protocol.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": reverse_lazy("describe:description-protocol"),
                "hx-trigger": "change"
            }
        ),
    )


DescriptionFilterFormSet = formset_factory(DescriptionFilterForm, extra=0)
