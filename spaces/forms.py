from django import forms

from spaces.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("name", "latitude", "longitude")
