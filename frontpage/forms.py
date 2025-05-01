from django import forms
from django.contrib.auth.forms import UserChangeForm, UsernameField
from django.contrib.auth.models import Group, User

from frontpage.widgets import TomSelectMultiple


class UserUpdateForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=TomSelectMultiple(),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_staff", "is_superuser", "groups")
