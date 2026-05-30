from django.test import TestCase

from describe.factories import DescriptionFactory, ProtocolFactory, WorkspaceElementFactory, WorkspaceFactory
from frontpage.factories import UserFactory
from frontpage.testcases import ViewSmokeTestMixin


class DescribeViewsSmokeTest(ViewSmokeTestMixin, TestCase):
    def setUp(self):
        self.app_name = "describe"
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.description = DescriptionFactory()
        self.workspace = WorkspaceFactory(user=self.user)
        self.protocol = ProtocolFactory()
        WorkspaceElementFactory.create_batch(2, workspace=self.workspace)

    def test_description_views(self):
        self.assert_get(["description_list", "description_compare"])
        self.assert_get(["description_detail", "description_expression_update"], [self.description.id])
        self.assert_post(["description_delete"], [self.description.id], status_code=302)
