from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, LayoutObject, Submit
from django import forms
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from frontpage.widgets import TomSelectMultiple


class AdminUserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=TomSelectMultiple(),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_staff", "is_superuser", "is_active", "groups")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class HTMXFormMixin:
    """
    Adds standard htmx+crispy GET‐filter helper to any Form or ModelForm.
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


def generate_form_layout(fields: list[Field], cols_lg=4):
    if not all(isinstance(field, Field) for field in fields):
        raise Exception("fields should be a list of crispy_forms.layout.Field objects")
    layout = Layout(
        Div(
            *[Div(field, css_class="col") for field in fields],
            css_class=f"row row-cols-lg-{cols_lg} align-items-top",
        ),
        Div(
            Submit("search", "Search", css_class="btn-sm"),
            HTML('<a class="btn btn-sm btn-secondary" href=".">Clear</a>'),
            css_class="mt-0 mb-3",
        ),
    )
    return layout


class SearchAndClearButtons(LayoutObject):
    def __init__(self, submit_name="search", submit_label="Search", css_class="mt-0 mb-3"):
        self.submit_name = submit_name
        self.submit_label = submit_label
        self.css_class = css_class

    def render(self, form, form_style, context, template_pack=None, **kwargs):
        layout = Div(
            Submit(self.submit_name, self.submit_label, css_class="btn-sm"),
            HTML(
                format_html(
                    '<a class="btn btn-sm btn-secondary" href="{}">Clear</a>',
                    context.get("request").path,
                )
            ),
            css_class=self.css_class,
        )
        return mark_safe(layout.render(form, form_style, context, template_pack))
