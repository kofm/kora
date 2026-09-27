from collect.models import Storage, StoragePosition
from frontpage.autocomplete import AutocompleteModelView


class StoragePositionAutocompleteView(AutocompleteModelView):
    model = StoragePosition
    value_fields = ["id"]
    search_fields = ["name", "storage__name"]
    ordering = ["storage__order", "storage__pk", "name", "pk"]

    def hook_queryset(self, queryset):
        queryset = queryset.select_related("storage").empty_positions_for_sample()
        return queryset


class StorageAutocompleteView(AutocompleteModelView):
    model = Storage
    value_fields = ["id"]
    search_fields = ["name"]
    ordering = ["order", "pk"]
