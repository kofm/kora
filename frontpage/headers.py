from dataclasses import dataclass

from django.db import models
from django.template.loader import render_to_string

from frontpage.utils.permissions import get_permission_from_instance, get_permission_from_opts


@dataclass(slots=True)
class HeaderAction:
    label: str
    url: str
    permission: str
    modal: bool = False
    disabled: bool = False
    disabled_message: str = ""


class BaseHeader:
    template_name = ""

    def __init__(self, request, *, actions=()):
        self.request = request
        self.actions = actions

    def get_actions(self):
        return [action for action in self.actions if self.request.user.has_perm(action.permission)]

    def get_context_data(self):
        return {"actions": self.get_actions()}

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


class ListHeader(BaseHeader):
    template_name = "frontpage/headers/list.html"

    def __init__(self, request, model, *, title=None, subtitle=None, modal=False, actions=()):
        if not isinstance(model, type) or not issubclass(model, models.Model):
            raise TypeError("ListHeader requires a Django model class.")

        super().__init__(request, actions=actions)
        self.model = model
        self.title = title or model._meta.verbose_name_plural.title()
        self.subtitle = subtitle
        self.modal = modal

    def get_create_url(self):
        method = getattr(self.model, "get_create_url", None)
        return method() if method else None

    def get_context_data(self):
        can_add = self.request.user.has_perm(get_permission_from_opts("add", self.model._meta))
        return {
            **super().get_context_data(),
            "title": self.title,
            "subtitle": self.subtitle,
            "create_url": self.get_create_url() if can_add else None,
            "modal": self.modal,
        }


class DetailHeader(BaseHeader):
    template_name = "frontpage/headers/detail.html"
    default_cant_delete_msg = "You can't remove this entry because it is associated to other data."

    def __init__(
        self,
        request,
        instance,
        *,
        title=None,
        subtitle=None,
        subtitle_emphasis=False,
        update_modal=False,
        delete_modal=False,
        show_id=False,
        actions=(),
    ):
        super().__init__(request, actions=actions)
        self.instance = instance
        self.title = title or str(instance)
        self.subtitle = subtitle
        self.subtitle_emphasis = subtitle_emphasis
        self.update_modal = update_modal
        self.delete_modal = delete_modal
        self.show_id = show_id

    def get_update_url(self):
        method = getattr(self.instance, "get_update_url", None)
        return method() if method else None

    def get_delete_url(self):
        method = getattr(self.instance, "get_delete_url", None)
        return method() if method else None

    def get_context_data(self):
        user = self.request.user
        can_update = user.has_perm(get_permission_from_instance("change", self.instance))
        can_delete = user.has_perm(get_permission_from_instance("delete", self.instance))
        is_deletable = getattr(self.instance, "is_deletable", True)
        if callable(is_deletable):
            is_deletable = is_deletable()

        return {
            **super().get_context_data(),
            **self._get_display_context(),
            "update_url": self.get_update_url() if can_update else None,
            "delete_url": self.get_delete_url() if can_delete else None,
            "is_deletable": is_deletable,
            "cant_delete_msg": getattr(self.instance, "cant_delete_msg", self.default_cant_delete_msg),
        }

    def _get_display_context(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "object": self.instance,
            "object_id": self.instance.pk if self.show_id else None,
            "subtitle_emphasis": self.subtitle_emphasis,
            "update_modal": self.update_modal,
            "delete_modal": self.delete_modal,
        }


class ArchivalDetailHeader(DetailHeader):
    template_name = "frontpage/headers/archival_detail.html"

    def get_archive_url(self):
        method = getattr(self.instance, "get_archive_url", None)
        return method() if method else None

    def get_restore_url(self):
        method = getattr(self.instance, "get_restore_url", None)
        return method() if method else None

    def get_context_data(self):
        can_change = self.request.user.has_perm(get_permission_from_instance("change", self.instance))
        is_archived = self.instance.is_archived

        return {
            **BaseHeader.get_context_data(self),
            **self._get_display_context(),
            "update_url": self.get_update_url() if can_change and not is_archived else None,
            "archive_url": self.get_archive_url() if can_change and not is_archived else None,
            "restore_url": self.get_restore_url() if can_change and is_archived else None,
        }
