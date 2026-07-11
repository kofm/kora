from rest_framework.renderers import BrowsableAPIRenderer


class NoWriteFormsBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Keep the DRF browsable API, but hide POST/PUT/PATCH forms.

    This also avoids the serializer/form construction that can trigger
    large query counts for relational select fields.
    """

    write_methods = {"POST", "PUT", "PATCH"}

    def show_form_for_method(self, view, method, request, obj):
        if method in self.write_methods and view.action != "excel_import":
            return False

        return super().show_form_for_method(view, method, request, obj)
