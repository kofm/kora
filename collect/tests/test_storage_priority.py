import json

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from collect.models import Storage


class StoragePriorityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("storage-admin", "admin@example.com", "password")
        self.client.force_login(self.user)

    def test_htmx_pagination_returns_replaceable_results_with_controls_outside_sort_form(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(101)]
        url = reverse("collect:storage_list")
        full_page = self.client.get(url, {"page": 2})
        self.assertContains(full_page, f'hx-get="{url}" hx-trigger="listChanged from:body"')
        self.assertContains(full_page, 'hx-target="#storage-results" hx-swap="outerHTML" hx-push-url="true"')

        response = self.client.get(url, {"page": 2}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        results = response.content.decode().strip()
        self.assertTrue(results.startswith('<section id="storage-results">'))
        self.assertTrue(results.endswith("</section>"))
        self.assertIn(f'name="order" value="{boxes[-1].pk}"', results)
        self.assertEqual(results.count('name="order"'), 1)
        self.assertIn('hx-trigger="end from:#storage-cards"', results)
        self.assertIn('hx-boost="true"', results.split("</form>", 1)[1])
        self.assertIn('href="?page=1"', results)

    def test_page_reorder_keeps_other_pages_and_existing_gaps(self):
        containers = [Storage.objects.append(Storage(name=f"Box {i:03}")) for i in range(102)]
        containers[1].delete()
        response = self.client.get(reverse("collect:storage_list"), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)
        self.assertContains(response, f'name="order" value="{containers[-1].pk}"')
        self.assertNotContains(response, f'name="order" value="{containers[0].pk}"')

        before = dict(Storage.objects.values_list("pk", "order"))
        # The first page has 100 items; swap two there without changing the second page.
        ids = list(Storage.objects.values_list("pk", flat=True)[:100])
        ids[0], ids[-1] = ids[-1], ids[0]
        response = self.client.post(reverse("collect:storage-sort"), {"order": ids})
        self.assertEqual(response.status_code, 200)
        after = dict(Storage.objects.values_list("pk", "order"))
        self.assertEqual(after[ids[0]], before[ids[-1]])
        self.assertEqual(after[ids[-1]], before[ids[0]])
        self.assertEqual(after[containers[-1].pk], before[containers[-1].pk])
        self.assertNotIn(1, after.values())  # Deleting a container need not close the gap.

    def test_send_to_top_moves_across_pages_without_closing_priority_gaps(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i:03}")) for i in range(102)]
        boxes[1].delete()
        before = set(Storage.objects.values_list("order", flat=True))

        response = self.client.post(
            reverse("collect:storage-sort-to-top", args=[boxes[-1].pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.headers["HX-Trigger"]), {"listChanged": True})
        self.assertEqual(Storage.objects.first().pk, boxes[-1].pk)
        self.assertEqual(set(Storage.objects.values_list("order", flat=True)), before)
        self.assertContains(self.client.get(reverse("collect:storage_list")), f'name="order" value="{boxes[-1].pk}"')

    def test_storage_cards_use_responsive_columns_without_outer_margins(self):
        Storage.objects.append(Storage(name="Box"))
        response = self.client.get(reverse("collect:storage_list"))
        self.assertContains(response, 'row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-3')
        self.assertContains(response, '<div class="col draggable">')
        self.assertContains(response, '<div class="border p-3 rounded-3 h-100">')

    def test_storage_card_menu_only_offers_to_top_to_editors(self):
        box = Storage.objects.append(Storage(name="Box"))
        url = reverse("collect:storage-sort-to-top", args=[box.pk])
        response = self.client.get(reverse("collect:storage_list"))
        self.assertContains(response, 'aria-label="Storage actions"')
        self.assertContains(response, f'type="button" class="dropdown-item" hx-post="{url}">Move to top</button>')

        viewer = User.objects.create_user("storage-viewer", password="password")
        viewer.user_permissions.add(Permission.objects.get(codename="view_storage"))
        self.client.force_login(viewer)
        response = self.client.get(reverse("collect:storage_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'aria-label="Storage actions"')
        self.assertNotContains(response, f'hx-post="{url}"')

    def test_send_to_top_requires_change_permission(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(2)]
        viewer = User.objects.create_user("storage-viewer", password="password")
        viewer.user_permissions.add(Permission.objects.get(codename="view_storage"))
        self.client.force_login(viewer)
        response = self.client.post(reverse("collect:storage-sort-to-top", args=[boxes[-1].pk]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Storage.objects.values_list("pk", flat=True)), [box.pk for box in boxes])

    def test_api_reorder_requires_complete_ids_and_handles_long_distance_move(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(3)]
        url = reverse("restapi:storage-reorder")
        before = dict(Storage.objects.values_list("pk", "order"))
        response = self.client.post(
            url, data=json.dumps({"order": [boxes[2].pk, boxes[0].pk]}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(dict(Storage.objects.values_list("pk", "order")), before)

        response = self.client.post(
            url, data=json.dumps({"order": [boxes[2].pk, boxes[0].pk, boxes[1].pk]}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(list(Storage.objects.values_list("pk", flat=True)), [boxes[2].pk, boxes[0].pk, boxes[1].pk])

    def test_api_reorder_requires_change_permission(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(2)]
        self.client.force_login(User.objects.create_user("storage-viewer", password="password"))
        response = self.client.post(
            reverse("restapi:storage-reorder"),
            data=json.dumps({"order": [boxes[1].pk, boxes[0].pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Storage.objects.values_list("pk", flat=True)), [box.pk for box in boxes])

    def test_creation_paths_append_after_gap(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(3)]
        boxes[1].delete()
        url = reverse("restapi:storage-list")
        single = self.client.post(url, data=json.dumps({"name": "Single", "order": 0}), content_type="application/json")
        self.assertEqual(single.status_code, 201)
        bulk = self.client.post(
            reverse("restapi:storage-bulk"),
            data=json.dumps([{"name": "Bulk A"}, {"name": "Bulk B"}]),
            content_type="application/json",
        )
        self.assertEqual(bulk.status_code, 201)
        created = self.client.post(reverse("collect:storage_create"), {"name": "UI Box", "positions": 2})
        self.assertEqual(created.status_code, 302)
        created_orders = Storage.objects.filter(name__in=["Single", "Bulk A", "Bulk B", "UI Box"])
        self.assertEqual(list(created_orders.values_list("order", flat=True)), [3, 4, 5, 6])
        self.assertEqual(Storage.objects.get(name="UI Box").total_positions, 2)
