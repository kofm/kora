from django import forms

from spaces.models import Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = ("location", "order")
