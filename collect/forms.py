from django import forms
from django.db.models import Q

from collect.models import SeedSample, StoragePosition

class SeedSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].queryset = StoragePosition.objects.filter(Q(seedsample__id=self.instance.pk) | Q(seedsample__isnull=True))

    class Meta:
        model=SeedSample
        fields=('variety', 'growing_season', 'position', 'notes')
