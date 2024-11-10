from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .utils import (
    add_breadcrumbs,
    create_breadcrumb,
    delete_breadcrumb,
    detail_breadcrumb,
    list_breadcrumb,
    update_breadcrumb,
)


class BaseBreadcrumbsMixin:
    @property
    def crumbs(self):
        raise NotImplementedError("Breadcrumbs should be defined")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return add_breadcrumbs(context, self.crumbs)


class CreateBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_breadcrumb(self.model), create_breadcrumb(self.model)]


class UpdateBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_breadcrumb(self.model), detail_breadcrumb(self.object), update_breadcrumb(self.object)]


class DeleteBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_breadcrumb(self.model), detail_breadcrumb(self.object), delete_breadcrumb(self.object)]


class DetailBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_breadcrumb(self.model), detail_breadcrumb(self.object)]


class ListBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_breadcrumb(self.model)]


class CrumbsCreateView(CreateBreadcrumbsMixin, CreateView):
    pass


class CrumbsUpdateView(UpdateBreadcrumbsMixin, UpdateView):
    pass


class CrumbsListView(ListBreadcrumbsMixin, ListView):
    pass


class CrumbsDeleteView(DeleteBreadcrumbsMixin, DeleteView):
    pass


class CrumbsDetailView(DetailBreadcrumbsMixin, DetailView):
    pass
