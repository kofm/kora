from .utils import add_crumbs, create_crumb, detail_crumb, list_crumb, update_crumb


class BaseBreadcrumbsMixin:
    @property
    def crumbs(self):
        raise NotImplementedError("Breadcrumbs should be defined")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return add_crumbs(context, self.crumbs)


class CreateBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_crumb(self.model), create_crumb(self.model)]


class UpdateBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_crumb(self.model), detail_crumb(self.object), update_crumb(self.object)]


class DetailBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_crumb(self.model), detail_crumb(self.object)]


class ListBreadcrumbsMixin(BaseBreadcrumbsMixin):
    @property
    def crumbs(self):
        return [list_crumb(self.model)]
