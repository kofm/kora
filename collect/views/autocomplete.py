from django.db.models import CharField, Value
from django.db.models.functions import Concat

from collect.models import StoragePosition
from frontpage.autocomplete import AutocompleteModelView


class StoragePositionAutocompleteView(AutocompleteModelView):
    model = StoragePosition
    value_fields = ["id", "name", "text"]

    def hook_queryset(self, queryset):
        queryset = queryset.annotate(
            text=Concat(
                "storage__name",
                Value("-"),
                "name",
                output_field=CharField(),
            )
        ).empty_positions_for_sample()
        return queryset
