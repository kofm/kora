from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, LayoutObject, Submit
from django import forms
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from frontpage.widgets import ModelTomSelect, TomSelectMultiple


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
    hx_trigger: str = "change, input delay:500ms"
    form_method: str = "GET"

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


class TomSelectModelFormMixin:
    """Initialize querysets for dependent TomSelect fields.

    To provide correct validation to dependant fields when using
    remote TomSelect widgets it is better to set the initial queryset
    as `none()`. This mixin correctly initialise the querysets of the
    dependant fields when the value(s) from which they depend on is
    set in the form. This ensure that the submitted value is validated
    against the filtered data instead of the full table. This mixin is
    not necessary if there are no dependant TomSelect fields.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = self.fields
        for _, field in fields.items():
            widget = field.widget
            if not isinstance(widget, ModelTomSelect):
                continue

            depends_on = widget.ts_config.depends_on()
            lookup_field = widget.ts_config.depends_param()

            if not depends_on:
                continue
            value = self._field_value(depends_on)
            if value:
                field.queryset = field.queryset.model.objects.filter(**{lookup_field: value})

    def _field_value(self, field_name):
        if self.is_bound:
            value = self.data.get(self.add_prefix(field_name))
        else:
            value = self.initial.get(field_name)

        if hasattr(value, "pk"):
            return value.pk

        return value
