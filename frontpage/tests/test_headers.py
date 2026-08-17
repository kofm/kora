from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase

from calculator.factories import CropLayoutFactory
from frontpage.factories import UserFactory
from frontpage.headers import ArchivalDetailHeader, DetailHeader, HeaderAction, ListHeader
from register.factories import EntityFactory
from register.models import Entity


class HeaderTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def request_for(self, user):
        request = self.request_factory.get("/")
        request.user = user
        return request

    def permission(self, app_label, codename):
        return Permission.objects.get(content_type__app_label=app_label, codename=codename)

    def test_list_header_filters_supported_actions_by_add_permission(self):
        user = UserFactory()

        entity_context = ListHeader(self.request_for(user), Entity).get_context_data()
        self.assertIsNone(entity_context["create_url"])

        user.user_permissions.add(
            self.permission("register", "add_entity"),
            self.permission("register", "add_protection"),
        )
        user = type(user).objects.get(pk=user.pk)

        entity_context = ListHeader(self.request_for(user), Entity).get_context_data()
        self.assertEqual(entity_context["create_url"], Entity.get_create_url())

    def test_detail_header_filters_update_and_delete_by_separate_permissions(self):
        instance = EntityFactory()
        update_user = UserFactory()
        update_user.user_permissions.add(self.permission("register", "change_entity"))
        delete_user = UserFactory()
        delete_user.user_permissions.add(self.permission("register", "delete_entity"))

        update_context = DetailHeader(self.request_for(update_user), instance).get_context_data()
        self.assertEqual(update_context["update_url"], instance.get_update_url())
        self.assertIsNone(update_context["delete_url"])

        delete_context = DetailHeader(self.request_for(delete_user), instance).get_context_data()
        self.assertIsNone(delete_context["update_url"])
        self.assertEqual(delete_context["delete_url"], instance.get_delete_url())

    def test_archival_detail_header_exposes_actions_for_the_lifecycle_state(self):
        user = UserFactory()
        active = CropLayoutFactory()
        archived = CropLayoutFactory()
        archived.archive()

        read_only_context = ArchivalDetailHeader(self.request_for(user), active).get_context_data()
        self.assertIsNone(read_only_context["update_url"])
        self.assertIsNone(read_only_context["archive_url"])
        self.assertIsNone(read_only_context["restore_url"])

        user.user_permissions.add(self.permission("calculator", "change_croplayout"))
        user = type(user).objects.get(pk=user.pk)
        active_context = ArchivalDetailHeader(self.request_for(user), active).get_context_data()
        self.assertEqual(active_context["update_url"], active.get_update_url())
        self.assertEqual(active_context["archive_url"], active.get_archive_url())
        self.assertIsNone(active_context["restore_url"])

        archived_context = ArchivalDetailHeader(self.request_for(user), archived).get_context_data()
        self.assertIsNone(archived_context["update_url"])
        self.assertIsNone(archived_context["archive_url"])
        self.assertEqual(archived_context["restore_url"], archived.get_restore_url())

    def test_context_uses_overridden_url_hook(self):
        class CustomDetailHeader(DetailHeader):
            def get_update_url(self):
                return "/custom-update/"

        user = UserFactory()
        user.user_permissions.add(self.permission("register", "change_entity"))

        context = CustomDetailHeader(self.request_for(user), EntityFactory()).get_context_data()

        self.assertEqual(context["update_url"], "/custom-update/")

    def test_header_renders_only_permitted_actions_and_hides_empty_menu(self):
        permitted_action = HeaderAction(
            label="Permitted action",
            url="/permitted/",
            permission="register.change_entity",
        )
        forbidden_action = HeaderAction(
            label="Forbidden action",
            url="/forbidden/",
            permission="register.delete_entity",
        )
        user = UserFactory()
        request = self.request_for(user)

        content = ListHeader(request, Entity, actions=[permitted_action, forbidden_action]).render()
        self.assertNotIn('aria-label="More actions"', content)

        user.user_permissions.add(self.permission("register", "change_entity"))
        user = type(user).objects.get(pk=user.pk)
        content = ListHeader(
            self.request_for(user),
            Entity,
            actions=[permitted_action, forbidden_action],
        ).render()

        self.assertIn('aria-label="More actions"', content)
        self.assertIn('href="/permitted/"', content)
        self.assertNotIn("Forbidden action", content)

    def test_detail_header_preserves_normal_and_modal_action_behavior(self):
        user = UserFactory()
        user.user_permissions.add(self.permission("register", "change_entity"))
        actions = [
            HeaderAction(
                label="Normal action",
                url="/normal/",
                permission="register.change_entity",
            ),
            HeaderAction(
                label="Modal action",
                url="/modal/",
                permission="register.change_entity",
                modal=True,
            ),
        ]

        content = DetailHeader(self.request_for(user), EntityFactory(), actions=actions).render()

        self.assertIn('href="/normal/"', content)
        self.assertIn('hx-get="/modal/"', content)
        self.assertIn('data-bs-target="#modal"', content)
