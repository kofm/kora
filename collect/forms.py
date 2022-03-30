from django import forms
from django.db.models import Q
from django.forms.widgets import HiddenInput, TextInput

from collect.models import Germinability, SampleWeight, SeedSample, StoragePosition

class SeedSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].queryset = StoragePosition.objects.filter(Q(seedsample__id=self.instance.pk) | Q(seedsample__isnull=True))

    class Meta:
        model=SeedSample
        fields=('sample_id', 'variety', 'growing_season', 'position', 'notes')
        widgets={
            'variety': HiddenInput(),
            'position': TextInput()
        }

class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ('weight', )

class GerminabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(GerminabilityForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['germinability'].required = False
    class Meta:
        model = Germinability
        fields = ('germinability', 'after_days', 'performed_at')
