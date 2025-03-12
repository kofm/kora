from django.urls import path

import describe.views.description as dsc
import describe.views.expression as xpr
import describe.views.protocol as prt
import describe.views.state as stt
import describe.views.trait as trt
import describe.views.workspace as wsp

app_name = "describe"

urlpatterns = [
    path("", dsc.description_list, name="description_list"),
    path("filter", dsc.description_filter, name="description_filter"),
    path("find-similar", dsc.description_find_similar, name="description_find_similar"),
    path("workspace/create", wsp.workspace_create, name="workspace_create"),
    path("workspace/", wsp.workspace_list, name="workspace_list"),
    path("workspace/<int:pk>/update", wsp.workspace_update, name="workspace_update"),
    path("workspace/<int:pk>/delete", wsp.workspace_delete, name="workspace_delete"),
    path("workspace/activate", wsp.workspace_activate, name="workspace_activate"),
    path("workspace/element/create", wsp.workspace_element_create, name="workspace_element_create"),
    path("workspace/element/<int:pk>/delete", wsp.workspace_element_delete, name="workspace_element_delete"),
    path("workspace/sort", wsp.WorkspaceSortableView.as_view(), name="workspace_sort"),
    path("compare", dsc.description_compare, name="description-compare"),
    path("export", dsc.description_filter_export, name="description-list-export"),
    path("export/download", dsc.description_filter_export_download, name="description_filter_export_download"),
    path("<int:pk>/", dsc.DescriptionDetail.as_view(), name="description_detail"),
    path("<int:pk>/expressions/update", dsc.description_expression_update, name="description_expression_update"),
    path("<int:pk>/update", dsc.description_update, name="description_update"),
    path("create", dsc.description_create, name="description_create"),
    path("<int:pk>/delete", dsc.DescriptionDeleteView.as_view(), name="description_delete"),
    path("protocols/", prt.ProtocolList.as_view(), name="protocol_list"),
    path("protocols/<int:pk>/", prt.ProtocolDetail.as_view(), name="protocol_detail"),
    path("protocols/<int:pk>/update", prt.protocol_update, name="protocol_update"),
    path("protocols/<int:pk>/update_meta", prt.protocol_update_meta, name="protocol_update_meta"),
    path("protocols/create", prt.ProtocolCreate.as_view(), name="protocol_create"),
    path("protocols/<int:pk>/delete", prt.ProtocolDelete.as_view(), name="protocol_delete"),
    path("traits/", trt.related_state_form, name="trait_list"),
    path("traits/<int:pk>/update", trt.trait_update, name="trait_update"),
    path("traits/<int:pk>/delete", trt.trait_delete, name="trait_delete"),
    path("protocol/<int:protocol_pk>/trait/create", trt.trait_create, name="trait_create"),
    path("state/<int:pk>/update", stt.state_update, name="state-update"),
    path("state/<int:pk>/delete", stt.state_delete, name="state_delete"),
    path("state/<int:pk>/update2", stt.state_update2, name="state_update2"),
    path("trait/<int:trait_pk>/state/form", stt.state_form, name="state_form"),
    path("state/create", stt.state_create, name="state_create"),
    path("state/<int:pk>/related_state/delete", stt.relatedstate_delete, name="relatedstate-delete"),
    path("expression/<int:pk>/update", xpr.expression_update_form, name="expression-update"),
    path(
        "<int:pk>/trait/<int:trait>/expression/form",
        xpr.expression_create_form_empty,
        name="description-expression-form",
    ),
    path("expression/<int:pk>/delete", xpr.expression_delete, name="expression-delete"),
    path("expression/create", xpr.expression_create, name="expression-create"),
]
