from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from calculator.factories import ManagementFactory
from calculator.models import ManagementType
from frontpage.factories import UserFactory


class ManagementTypeDeleteTests(TestCase):
    def test_referenced_type_direct_deletion_is_handled(self):
        user = UserFactory(username="management-type-deleter", password="x")
        user.user_permissions.add(
            Permission.objects.get(codename="delete_managementtype"),
            Permission.objects.get(codename="view_managementtype"),
        )
        self.client.force_login(user)
        management_type = ManagementFactory().type

        response = self.client.post(
            reverse("calculator:managementtype_delete", args=(management_type.pk,)),
            follow=True,
        )

        self.assertRedirects(response, reverse("calculator:managementtype_list"))
        self.assertTrue(ManagementType.objects.filter(pk=management_type.pk).exists())
        self.assertIn(
            management_type.cant_delete_msg, [message.message for message in get_messages(response.wsgi_request)]
        )
