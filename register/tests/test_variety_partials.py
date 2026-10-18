from inspect import unwrap

from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from frontpage.factories import UserFactory
from frontpage.views_decorators import public_catalog_view
from register.factories import PlantVarietyFactory
from register.views.plantvariety_views import plantvariety_detail


class VarietyPartialPermissionsTests(TestCase):
    @override_settings(PUBLIC=True)
    def test_private_sections_require_permission_even_for_direct_public_catalog_requests(self):
        variety = PlantVarietyFactory()
        user = UserFactory()
        user.user_permissions.add(Permission.objects.get(codename="view_plantvariety"))
        # Public access is selected when the decorator is applied, not at request time.
        view = public_catalog_view("register.view_plantvariety")(unwrap(plantvariety_detail))
        factory = RequestFactory()
        for visitor in (AnonymousUser(), user):
            for section in ("descriptions", "names", "protections", "samples", "parameters"):
                with self.subTest(visitor=visitor, section=section):
                    request = factory.get(
                        reverse("register:variety_detail", args=[variety.pk]),
                        {"partial": section},
                        HTTP_HX_REQUEST="true",
                    )
                    request.user = visitor
                    if section in ("samples", "parameters"):
                        with self.assertRaises(PermissionDenied):
                            view(request, variety.pk)
                    else:
                        self.assertEqual(view(request, variety.pk).status_code, 200)
