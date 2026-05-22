from django.db.models import Count

from frontpage.autocomplete import AutocompleteModelView
from register.models import Entity, PlantSpecies, PlantVariety


class PlantSpeciesAutocompleteView(AutocompleteModelView):
    model = PlantSpecies
    search_fields = ["common_name", "latin_name"]
    value_fields = ["id", "common_name", "latin_name"]
    ordering = ["-num_var", "common_name"]

    def hook_queryset(self, queryset):
        return queryset.annotate(num_var=Count("variety"))


class PlantVarietyAutocompleteView(AutocompleteModelView):
    model = PlantVariety
    filter_by = ["species_id"]


class EntityAutocompleteView(AutocompleteModelView):
    model = Entity
