from django import forms

from collect.models import SeedSample

class SeedSampleForm(forms.ModelForm):

    class Meta:
        model=SeedSample
        fields=('variety', 'notes')
