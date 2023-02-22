from django import forms

from spaces.models import Area, Location

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
