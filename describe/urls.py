from django.urls import path
from . import views

app_name = "describe"

urlpatterns = [
    path("", views.description_list, name="description-list"),
    path("reset", views.description_list_reset, name="description-list-reset"),
    path("find_similar", views.description_find_similar, name="description-find-similar"),
    path(
        "add_favourite",
        views.description_favourite_add,
        name="description-favourite-add",
    ),
    path(
        "clear_favourites",
        views.description_favourite_clear,
        name="description-favourites-clear",
    ),
    path("compare", views.description_compare, name="description-compare"),
    path("export", views.description_filter_export, name="description-list-export"),
    path("<int:pk>/", views.DescriptionDetail.as_view(), name="description-detail"),
    path("<int:pk>/update", views.description_update_expressions, name="description-update"),
    path("<int:pk>/update_meta", views.description_update, name="description-update-metadata"),
    path("create", views.description_create, name="description-create"),
    path(
        "<int:pk>/delete",
        views.DescriptionDeleteView.as_view(),
        name="description-delete",
    ),
    path("protocols/", views.ProtocolList.as_view(), name="protocols_list"),
    path("protocols/<int:pk>/", views.protocol_detail, name="protocol_detail"),
    path("protocols/<int:pk>/update", views.protocol_update, name="protocol-update"),
    path(
        "protocols/<int:pk>/update_name",
        views.protocol_update_name_htmx,
        name="protocol-updatename",
    ),
    path("protocols/create", views.ProtocolCreate.as_view(), name="protocol-create"),
    path(
        "protocols/<int:pk>/delete",
        views.ProtocolDelete.as_view(),
        name="protocol-delete",
    ),
    # Trait
    path("traits/", views.related_state_form, name="trait-list"),
    # State
    path("state/<int:pk>/update", views.state_update, name="state-update"),
    path(
        "state/<int:pk>/related_state/delete",
        views.relatedstate_delete,
        name="relatedstate-delete",
    ),
    path("expression/<int:pk>/update", views.expression.expression_update, name="expression-update"),
    path(
        "<int:pk>/trait/<int:trait>/expression/form",
        views.expression.expression_form,
        name="description-expression-form",
    ),
    path("expression/<int:pk>/delete", views.expression.expression_delete, name="expression-delete"),
    path("expression/create", views.expression.expression_create, name="expression-create"),
]
