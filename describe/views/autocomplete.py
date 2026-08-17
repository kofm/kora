from describe.models import Protocol, State, Trait
from frontpage.autocomplete import AutocompleteModelView


class ProtocolAutocompleteView(AutocompleteModelView):
    model = Protocol
    ordering = ["order"]
    filter_by = ["plantspecies_id"]


class TraitAutocompleteView(AutocompleteModelView):
    model = Trait
    search_fields = ["numeric_id", "description"]
    value_fields = ["id", "numeric_id", "description"]
    filter_by = ["protocol_id"]
    ordering = ["numeric_id", "pk"]


class StateAutocompleteView(AutocompleteModelView):
    model = State
    search_fields = ["numeric_id", "description"]
    value_fields = ["id", "numeric_id", "description"]
    filter_by = ["trait_id"]
    ordering = ["numeric_id", "pk"]
