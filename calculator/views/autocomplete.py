from calculator.models import CropLayout
from frontpage.autocomplete import AutocompleteModelView


class CropLayoutAutocompleteView(AutocompleteModelView):
    model = CropLayout
    filter_by = ["location_id"]
    ordering = ["name", "pk"]

    def hook_queryset(self, queryset):
        return queryset.visible()
