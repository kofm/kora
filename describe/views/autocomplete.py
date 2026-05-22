
from describe.models import Protocol
from frontpage.autocomplete import AutocompleteModelView


class ProtocolAutocompleteView(AutocompleteModelView):
    model = Protocol
    ordering = ["order"]
    filter_by = ["plantspecies_id"]
