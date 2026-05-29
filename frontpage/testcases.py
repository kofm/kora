from django.urls import reverse


class ViewSmokeTestMixin:
    app_name = None

    def assert_get(self, view_names, reverse_args=None, status_code=200):
        self._assert_response("get", view_names, reverse_args, status_code)

    def assert_post(self, view_names, reverse_args=None, status_code=200):
        self._assert_response("post", view_names, reverse_args, status_code)

    def _assert_response(self, method, view_names, reverse_args=None, status_code=200):
        reverse_args = reverse_args or []

        for name in view_names:
            with self.subTest(view=name, method=method.upper()):
                url = reverse(f"{self.app_name}:{name}", args=reverse_args)
                response = getattr(self.client, method)(url)

                self.assertEqual(
                    status_code,
                    response.status_code,
                    f"Failing View: {name} ({method.upper()})",
                )
