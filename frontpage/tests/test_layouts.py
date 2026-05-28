from django.test import SimpleTestCase

from frontpage.utils.assets import _ensure_assets


class AssetsTest(SimpleTestCase):
    def setUp(self):
        self.context = {}

    def test_assets_structure_is_ensured_in_context(self):
        assets = _ensure_assets(self.context)
        self.assertEqual({"css": [], "js": [], "hs": []}, assets)
        self.assertEqual({"template_assets": {"css": [], "js": [], "hs": []}}, self.context)
