from . import models
from django import forms
from django.forms import formset_factory, inlineformset_factory

class TraitForm(forms.Form):
    numeric_id = forms.IntegerField()
    description = forms.CharField()
    protocol_id = forms.IntegerField(widget=forms.HiddenInput)


TraitFormSet = inlineformset_factory(
        models.Protocol,
        models.Trait,
        extra=1,
        fields=('numeric_id', 'description',)
        )
