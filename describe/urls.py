"""Describe URL endpoints."""

from django.urls import path

import describe.views.workspace as wsp
from describe import views

app_name = "describe"

urlpatterns = [
    path("", views.description_list, name="description_list"),
    path("reset", views.description_list_reset, name="description-list-reset"),
    path("find_similar", views.description_find_similar, name="description-similar"),
    path("workspace/create", views.workspace_create, name="workspace_create"),
    path("workspace/", wsp.workspace_list, name="workspace_list"),
    path("workspace/<int:pk>/update", views.workspace_update, name="workspace_update"),
    path("workspace/<int:pk>/delete", views.workspace_delete, name="workspace_delete"),
    path("workspace/activate", wsp.workspace_activate, name="workspace_activate"),
    path("workspace/element/create", views.workspace_element_create, name="workspace_element_create"),
    path("workspace/element/<int:pk>/delete", views.workspace_element_delete, name="workspace_element_delete"),
    path("workspace/sort", views.WorkspaceSortableView.as_view(), name="workspace_sort"),
    path("compare", views.description_compare, name="description-compare"),
    path("export", views.description_filter_export, name="description-list-export"),
    path("<int:pk>/", views.DescriptionDetail.as_view(), name="description_detail"),
    path("<int:pk>/expressions/update", views.description_expression_update, name="description_expression_update"),
    path("<int:pk>/update", views.description_update, name="description_update"),
    path("create", views.description_create, name="description_create"),
    path("<int:pk>/delete", views.DescriptionDeleteView.as_view(), name="description_delete"),
    path("protocols/", views.ProtocolList.as_view(), name="protocol_list"),
    path("protocols/<int:pk>/", views.ProtocolDetail.as_view(), name="protocol_detail"),
    path("protocols/<int:pk>/update", views.protocol_update, name="protocol_update"),
    path("protocols/<int:pk>/update_meta", views.protocol_update_meta, name="protocol_update_meta"),
    path("protocols/create", views.ProtocolCreate.as_view(), name="protocol_create"),
    path("protocols/<int:pk>/delete", views.ProtocolDelete.as_view(), name="protocol_delete"),
    path("traits/", views.related_state_form, name="trait_list"),
    path("traits/<int:pk>/update", views.trait_update, name="trait_update"),
    path("traits/<int:pk>/delete", views.trait_delete, name="trait_delete"),
    path("protocol/<int:protocol_pk>/trait/create", views.trait_create, name="trait_create"),
    path("state/<int:pk>/update", views.state_update, name="state-update"),
    path("state/<int:pk>/delete", views.state_delete, name="state_delete"),
    path("state/<int:pk>/update2", views.state_update2, name="state_update2"),
    path("trait/<int:trait_pk>/state/form", views.state_form, name="state_form"),
    path("state/create", views.state_create, name="state_create"),
    path("state/<int:pk>/related_state/delete", views.relatedstate_delete, name="relatedstate-delete"),
    path("expression/<int:pk>/update", views.expression.expression_update_form, name="expression-update"),
    path(
        "<int:pk>/trait/<int:trait>/expression/form",
        views.expression.expression_create_form_empty,
        name="description-expression-form",
    ),
    path("expression/<int:pk>/delete", views.expression.expression_delete, name="expression-delete"),
    path("expression/create", views.expression.expression_create, name="expression-create"),
]
