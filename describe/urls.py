from django.urls import path

import describe.views.autocomplete as ac
import describe.views.description as dsc
import describe.views.expression as xpr
import describe.views.protocol as prt
import describe.views.state as stt
import describe.views.trait as trt
import describe.views.workspace as wsp

app_name = "describe"

urlpatterns = [
    path("", dsc.description_list, name="description_list"),
    path("descriptions/form", dsc.description_form, name="description_form"),
    path("descriptions/find-similar", dsc.description_find_similar, name="description_find_similar"),
    path("descriptions/create", dsc.description_create, name="description_create"),
    path("descriptions/<int:pk>/delete", dsc.DescriptionDeleteView.as_view(), name="description_delete"),
    path("descriptions/<int:pk>/", dsc.description_detail, name="description_detail"),
    path("descriptions/<int:pk>/duplicate", dsc.description_duplicate, name="description_duplicate"),
    path("descriptions/configure", dsc.description_configure, name="description_configure"),
    path("description-label/<int:pk>/update", dsc.description_label_update, name="description_label_update"),
    path("workspace/create", wsp.workspace_create, name="workspace_create"),
    path("workspace/", wsp.workspace_detail, name="workspace_detail"),
    path("workspace/<int:pk>/update", wsp.workspace_update, name="workspace_update"),
    path("workspace/<int:pk>/delete", wsp.workspace_delete, name="workspace_delete"),
    path("workspace/activate", wsp.workspace_activate, name="workspace_activate"),
    path("workspace/element/create", wsp.workspace_element_create, name="workspace_element_create"),
    path("workspace/element/<int:pk>/delete", wsp.workspace_element_delete, name="workspace_element_delete"),
    path("workspace/sort", wsp.WorkspaceSortableView.as_view(), name="workspace_sort"),
    path("workspace/compare", dsc.description_compare, name="description_compare"),
    path(
        "descriptions/<int:pk>/expressions/update",
        dsc.description_expression_update,
        name="description_expression_update",
    ),
    path("protocols/", prt.protocol_list, name="protocol_list"),
    path("protocols/sort", prt.ProtocolSortView.as_view(), name="protocol_sort"),
    path("protocols/<int:pk>/", prt.protocol_detail, name="protocol_detail"),
    path("protocols/<int:pk>/update", prt.protocol_update, name="protocol_update"),
    path("protocols/<int:pk>/update-metadata", prt.protocol_update_meta, name="protocol_update_meta"),
    path("protocols/create", prt.ProtocolCreate.as_view(), name="protocol_create"),
    path("protocols/<int:pk>/delete", prt.ProtocolDelete.as_view(), name="protocol_delete"),
    path("protocols/autocomplete", ac.ProtocolAutocompleteView.as_view(), name="protocol_autocomplete"),
    path("traits/<int:pk>/update", trt.trait_update, name="trait_update"),
    path("traits/<int:pk>/delete", trt.trait_delete, name="trait_delete"),
    path("traits/<int:pk>/relate-states", trt.trait_relate_states, name="trait_relate_states"),
    path("states/<int:pk>/related-states-update", trt.state_related_states_update, name="state_related_states_update"),
    path(
        "states/<int:pk>/related-states-bulk-delete",
        trt.state_related_states_bulk_delete,
        name="state_related_states_bulk_delete",
    ),
    path(
        "traits/<int:pk>/states/related-states-reset",
        trt.trait_states_related_states_reset,
        name="trait_states_related_states_reset",
    ),
    path("states/<int:pk>/remove-from-group", trt.state_related_states_delete, name="state_reset_group"),
    path("traits/<int:trait_pk>/trait-state-form", stt.state_form, name="state_form"),
    path("traits/<int:pk>/bulk-relate-state", trt.trait_states_bulk_relate, name="trait_states_bulk_relate"),
    path("protocols/<int:protocol_pk>/create-trait", trt.trait_create, name="trait_create"),
    path("states/<int:pk>/delete", stt.state_delete, name="state_delete"),
    path("states/search", trt.state_sortable_source_list, name="state_search"),
    path("states/create", stt.state_create, name="state_create"),
    path("expressions/<int:pk>/update", xpr.expression_update, name="expression-update"),
    path("expressions/<int:pk>/delete", xpr.expression_delete, name="expression-delete"),
    path("expressions/create", xpr.expression_create, name="expression-create"),
]
