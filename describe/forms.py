from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from . import models


class TraitForm(forms.Form):
    numeric_id = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    protocol_id = forms.IntegerField(widget=forms.HiddenInput)


StateFormset = inlineformset_factory(
    models.Trait,
    models.State,
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
    models.Protocol,
    models.Trait,
    formset=BaseTraitFormSet,
    extra=1,
    fields=(
        "numeric_id",
        "description",
    ),
)


class ExpressionForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    state_of_expression = forms.ModelChoiceField(queryset=models.State.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpressionForm, self).__init__(*args, **kwargs)
        self.fields["state_of_expression"].required = False
        self.fields["id"].required = False
