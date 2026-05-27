from collect.models import StoragePosition
from frontpage.autocomplete import AutocompleteModelView


class StoragePositionAutocompleteView(AutocompleteModelView):
    model = StoragePosition
    value_fields = ["id"]
    search_fields = ["name", "storage__name"]

    def hook_queryset(self, queryset):
        queryset = queryset.select_related("storage")
        return queryset
