import json

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from collect.models import Storage


class StoragePriorityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("storage-admin", "admin@example.com", "password")
        self.client.force_login(self.user)

    def test_storage_list_paginates_for_full_and_htmx_requests(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(101)]
        url = reverse("collect:storage_list")
        for headers in ({}, {"HTTP_HX_REQUEST": "true"}):
            response = self.client.get(url, {"page": 2}, **headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual([box.pk for box in response.context["object_list"]], [boxes[-1].pk])

    def test_page_reorder_keeps_other_pages_and_existing_gaps(self):
        containers = [Storage.objects.append(Storage(name=f"Box {i:03}")) for i in range(102)]
        containers[1].delete()
        response = self.client.get(reverse("collect:storage_list"), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)

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
            reverse("collect:storage_move_to_boundary", args=[boxes[-1].pk]),
            {"boundary": "top"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.headers["HX-Trigger"]), {"listChanged": True})
        self.assertEqual(Storage.objects.first().pk, boxes[-1].pk)
        self.assertEqual(set(Storage.objects.values_list("order", flat=True)), before)

    def test_move_requires_change_permission(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(2)]
        viewer = User.objects.create_user("storage-viewer", password="password")
        viewer.user_permissions.add(Permission.objects.get(codename="view_storage"))
        self.client.force_login(viewer)
        boundary_url = reverse("collect:storage_move_to_boundary", args=[boxes[-1].pk])
        before_url = reverse("collect:storage_move_to", args=[boxes[-1].pk])
        for response in (
            self.client.post(boundary_url, {"boundary": "top"}),
            self.client.get(before_url),
            self.client.post(before_url, {"storage": boxes[0].pk}),
        ):
            self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Storage.objects.values_list("pk", flat=True)), [box.pk for box in boxes])

    def test_move_before_in_both_directions_and_to_bottom_preserves_priorities(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(5)]
        boxes[1].delete()  # Moving containers must not close priority gaps.
        priorities = set(Storage.objects.values_list("order", flat=True))

        def before_url(box):
            return reverse("collect:storage_move_to", args=[box.pk])

        response = self.client.post(before_url(boxes[4]), {"storage": boxes[2].pk}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.headers["HX-Trigger"]), {"closeModal": True, "listChanged": True})
        self.assertEqual(
            list(Storage.objects.values_list("pk", flat=True)), [boxes[0].pk, boxes[4].pk, boxes[2].pk, boxes[3].pk]
        )

        response = self.client.post(before_url(boxes[0]), {"storage": boxes[3].pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            list(Storage.objects.values_list("pk", flat=True)), [boxes[4].pk, boxes[2].pk, boxes[0].pk, boxes[3].pk]
        )

        response = self.client.post(
            reverse("collect:storage_move_to_boundary", args=[boxes[4].pk]), {"boundary": "bottom"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            list(Storage.objects.values_list("pk", flat=True)), [boxes[2].pk, boxes[0].pk, boxes[3].pk, boxes[4].pk]
        )
        self.assertEqual(set(Storage.objects.values_list("order", flat=True)), priorities)

    def test_invalid_moves_leave_order_unchanged(self):
        boxes = [Storage.objects.append(Storage(name=f"Box {i}")) for i in range(2)]
        before = list(Storage.objects.values_list("pk", "order"))
        boundary_url = reverse("collect:storage_move_to_boundary", args=[boxes[0].pk])
        before_url = reverse("collect:storage_move_to", args=[boxes[0].pk])

        self.assertEqual(self.client.post(boundary_url, {"boundary": "middle"}).status_code, 400)
        response = self.client.post(before_url, {"storage": 999999})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(self.client.post(before_url, {"storage": boxes[0].pk}).status_code, 302)
        self.assertEqual(list(Storage.objects.values_list("pk", "order")), before)
        self.assertEqual(self.client.post(boundary_url, {"boundary": "top"}).status_code, 302)
        self.assertEqual(
            self.client.post(
                reverse("collect:storage_move_to_boundary", args=[999999]), {"boundary": "top"}
            ).status_code,
            404,
        )
        self.assertEqual(self.client.get(reverse("collect:storage_move_to", args=[999999])).status_code, 404)

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
