from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm
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


class HTMXFormMixin:
    """
    Adds your standard htmx+crispy GET‐filter helper to any Form or ModelForm.
    """

    hx_url: str = ""
    hx_trigger: str = "change from:select, keyup changed delay:500ms from:input"
    form_method: str = "get"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {
            f"hx_{self.form_method}": self.hx_url,
            "hx_trigger": self.hx_trigger,
        }
        self.helper.form_method = self.form_method


def generate_form_layout(fields: list[Field]):
    if not all([isinstance(field, Field) for field in fields]):
        raise Exception("fields should be a list of crispy_forms.layout.Field objects")
    layout = Layout(
        Div(
            *[Div(field, css_class="col-3") for field in fields],
            css_class="row row-cols-lg-4 g-3 align-items-center",
        ),
        Div(
            Div(Submit("search", "Search"), css_class="col-12"),
            HTML('<a class="btn btn-secondary" href=".">Clear</a>'),
            css_class="row row-cols-lg-auto",
        ),
    )
    return layout
