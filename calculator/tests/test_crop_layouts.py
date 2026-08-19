from datetime import date

from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from calculator.factories import CropFactory, CropLayoutFactory, FieldBookFactory, StepFactory
from calculator.modelling import CropModel
from calculator.models import (
    Management,
    ManagementType,
    ParameterObservation,
    ParameterTarget,
    Step,
    TraitObservation,
    TraitTarget,
)
from calculator.utils import generate_zigzag_pairs
from describe.factories import ProtocolFactory, StateFactory, TraitFactory
from frontpage.factories import AdminFactory, UserFactory
from parameters.factories import ParameterFactory
from parameters.models import VarietalParameter
from register.factories import PlantSpeciesFactory, PlantVarietyFactory
from spaces.factories import LocationFactory


class CropModelParameterTests(TestCase):
    def test_parameter_is_resolved_from_variety(self):
        species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        variety = PlantVarietyFactory(name="A", species=species)
        crop = CropFactory(
            layout__name="Layout",
            layout__location__name="Site",
            variety=variety,
        )
        parameter = ParameterFactory(
            code="thermal-time",
            name="Thermal time",
            description="Thermal time requirement",
            measure_unit="degree days",
        )
        VarietalParameter.objects.create(variety=variety, parameter=parameter, value=125)
        crop_model = CropModel(crop)
        crop_model.inputs = [parameter.code]

        self.assertEqual(crop_model.get_parameter(parameter.code), 125)
        self.assertTrue(crop_model.can_run())


class ObservationIntegrityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="observer")
        cls.location = LocationFactory(name="Site")
        cls.layout = CropLayoutFactory(location=cls.location, name="Layout")
        cls.other_layout = CropLayoutFactory(location=cls.location, name="Other")
        cls.species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        cls.other_species = PlantSpeciesFactory(
            common_name="Rice",
            latin_name="Oryza",
            plant_type="herbaceous",
        )
        cls.variety = PlantVarietyFactory(name="A", species=cls.species)
        cls.other_variety = PlantVarietyFactory(name="B", species=cls.other_species)
        cls.crop = CropFactory(layout=cls.layout, variety=cls.variety)
        cls.other_crop = CropFactory(layout=cls.other_layout, variety=cls.other_variety)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Book")
        cls.step = StepFactory(fieldbook=cls.fieldbook, crop=cls.crop)
        cls.protocol = ProtocolFactory(name="Protocol", plantspecies=cls.species)
        cls.trait = TraitFactory(numeric_id=1, description="Height", protocol=cls.protocol)
        cls.state = StateFactory(numeric_id=1, description="Tall", trait=cls.trait)

    def test_step_crop_must_belong_to_fieldbook_layout(self):
        with self.assertRaises(ValidationError):
            Step.objects.create(fieldbook=self.fieldbook, crop=self.other_crop)

    def test_trait_target_must_match_crop_species(self):
        other_protocol = ProtocolFactory(name="Rice protocol", plantspecies=self.other_species)
        other_trait = TraitFactory(numeric_id=1, description="Height", protocol=other_protocol)

        with self.assertRaises(ValidationError):
            TraitTarget.objects.create(step=self.step, trait=other_trait)

    def test_step_observation_must_match_crop_and_target(self):
        with self.assertRaises(ValidationError):
            TraitObservation.objects.create(crop=self.crop, state=self.state, created_by=self.user, step=self.step)

        TraitTarget.objects.create(step=self.step, trait=self.trait)
        with self.assertRaises(ValidationError):
            TraitObservation.objects.create(
                crop=self.other_crop,
                state=self.state,
                created_by=self.user,
                step=self.step,
            )

        observation = TraitObservation.objects.create(
            crop=self.crop,
            state=self.state,
            created_by=self.user,
            step=self.step,
        )
        self.assertEqual(observation.step, self.step)


class CalculatorPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="viewer", password="x")
        location = LocationFactory(name="Site")
        cls.layout = CropLayoutFactory(location=location, name="Layout")
        species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        variety = PlantVarietyFactory(name="A", species=species)
        cls.crop = CropFactory(layout=cls.layout, variety=variety)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Book")

    def setUp(self):
        self.client.force_login(self.user)

    def test_crop_and_fieldbook_details_require_view_permissions(self):
        response = self.client.get(self.crop.get_absolute_url())
        self.assertEqual(response.status_code, 403)
        response = self.client.get(self.fieldbook.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        self.user.user_permissions.add(Permission.objects.get(codename="view_crop"))
        response = self.client.get(self.crop.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.user.user_permissions.add(Permission.objects.get(codename="view_fieldbook"))
        response = self.client.get(self.fieldbook.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_fieldbook_creation_requires_add_permission(self):
        url = reverse("calculator:fieldbook_create", args=(self.layout.pk,))
        response = self.client.get(url, headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 403)

        self.user.user_permissions.add(Permission.objects.get(codename="add_fieldbook"))
        response = self.client.get(url, headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)

    def test_observer_can_record_without_fieldbook_planning_controls(self):
        protocol = ProtocolFactory(name="Wheat protocol", plantspecies=self.crop.variety.species)
        trait = TraitFactory(numeric_id=1, description="Height", protocol=protocol)
        StateFactory(numeric_id=1, description="Tall", trait=trait)
        step = StepFactory(fieldbook=self.fieldbook, crop=self.crop)
        target = TraitTarget.objects.create(step=step, trait=trait)
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_fieldbook"),
            Permission.objects.get(codename="view_step"),
            Permission.objects.get(codename="add_traitobservation"),
        )

        response = self.client.get(self.fieldbook.get_absolute_url())
        self.assertNotContains(response, "Configure fieldbook")
        self.assertNotContains(response, "data-selectable-grid")
        self.assertContains(response, step.get_absolute_url())

        response = self.client.get(step.get_absolute_url())
        self.assertContains(response, reverse("calculator:trait_observation_in_step_create", args=(step.pk,)))
        self.assertNotContains(response, reverse("calculator:trait_target_delete", args=(target.pk,)))

        self.user.user_permissions.add(Permission.objects.get(codename="change_fieldbook"))
        self.client.force_login(self.user)

        response = self.client.get(self.fieldbook.get_absolute_url())
        self.assertContains(response, "Configure fieldbook")
        self.assertContains(response, "data-selectable-grid")

        response = self.client.get(step.get_absolute_url())
        self.assertContains(response, reverse("calculator:trait_target_delete", args=(target.pk,)))


class TraitTargetCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AdminFactory(username="admin", password="x", is_superuser=True)
        cls.location = LocationFactory(name="Site")
        cls.layout = CropLayoutFactory(location=cls.location, name="Layout")
        cls.other_layout = CropLayoutFactory(location=cls.location, name="Other layout")
        cls.wheat = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        cls.rice = PlantSpeciesFactory(
            common_name="Rice",
            latin_name="Oryza",
            plant_type="herbaceous",
        )
        cls.wheat_variety = PlantVarietyFactory(name="Wheat variety", species=cls.wheat)
        cls.rice_variety = PlantVarietyFactory(name="Rice variety", species=cls.rice)
        cls.wheat_crop = CropFactory(layout=cls.layout, variety=cls.wheat_variety, order=0)
        cls.rice_crop = CropFactory(layout=cls.layout, variety=cls.rice_variety, order=1)
        cls.outside_crop = CropFactory(layout=cls.other_layout, variety=cls.wheat_variety, order=0)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Book")
        cls.protocol = ProtocolFactory(name="Wheat protocol", plantspecies=cls.wheat)
        cls.trait = TraitFactory(numeric_id=1, description="Height", protocol=cls.protocol)

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse("calculator:trait_target_create", args=(self.fieldbook.pk,))
        self.payload = {"protocol": self.protocol.pk, "trait": self.trait.pk}

    def test_incompatible_crops_are_skipped(self):
        response = self.client.post(
            self.url,
            {**self.payload, "selection": [self.wheat_crop.pk, self.rice_crop.pk]},
            follow=True,
        )

        self.assertRedirects(response, self.fieldbook.get_absolute_url())
        self.assertTrue(TraitTarget.objects.filter(step__crop=self.wheat_crop, trait=self.trait).exists())
        self.assertFalse(Step.objects.filter(fieldbook=self.fieldbook, crop=self.rice_crop).exists())
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertTrue(any("1 incompatible crop" in message for message in messages))

    def test_selection_must_belong_to_fieldbook_layout(self):
        response = self.client.post(
            self.url,
            {**self.payload, "selection": [self.wheat_crop.pk, self.outside_crop.pk]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Step.objects.filter(fieldbook=self.fieldbook).exists())

    def test_fieldbook_change_permission_authorizes_planning_instead_of_target_permission(self):
        user = UserFactory(username="planner", password="x")
        self.client.force_login(user)
        payload = {**self.payload, "selection": [self.wheat_crop.pk]}

        user.user_permissions.add(Permission.objects.get(codename="add_traittarget"))
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename="change_fieldbook"))
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.fieldbook.get_absolute_url())
        target = TraitTarget.objects.get(step__crop=self.wheat_crop, trait=self.trait)

        response = self.client.post(reverse("calculator:trait_target_delete", args=(target.pk,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, target.step.get_absolute_url())
        self.assertFalse(TraitTarget.objects.filter(pk=target.pk).exists())


class TargetDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AdminFactory(username="admin", password="x", is_superuser=True)
        cls.layout = CropLayoutFactory(name="Layout")
        cls.species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        cls.variety = PlantVarietyFactory(name="Wheat variety", species=cls.species)
        cls.crop = CropFactory(layout=cls.layout, variety=cls.variety)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Book")
        cls.step = StepFactory(fieldbook=cls.fieldbook, crop=cls.crop)
        cls.protocol = ProtocolFactory(name="Wheat protocol", plantspecies=cls.species)
        cls.trait = TraitFactory(numeric_id=1, description="Height", protocol=cls.protocol)
        cls.state = StateFactory(numeric_id=1, description="Tall", trait=cls.trait)
        cls.parameter = ParameterFactory(code="weight", name="Weight")

    def setUp(self):
        self.client.force_login(self.user)

    def test_observed_targets_cannot_be_deleted_individually(self):
        trait_target = TraitTarget.objects.create(step=self.step, trait=self.trait)
        parameter_target = ParameterTarget.objects.create(step=self.step, parameter=self.parameter)
        TraitObservation.objects.create(
            crop=self.crop,
            step=self.step,
            state=self.state,
            created_by=self.user,
        )
        ParameterObservation.objects.create(
            crop=self.crop,
            step=self.step,
            parameter=self.parameter,
            parameter_value=1,
            created_by=self.user,
        )

        requests = (
            ("calculator:trait_target_delete", trait_target),
            ("calculator:parameter_target_delete", parameter_target),
        )
        for url_name, target in requests:
            with self.subTest(url_name=url_name):
                response = self.client.post(reverse(url_name, args=(target.pk,)))

                self.assertEqual(response.status_code, 400)
                self.assertTrue(type(target).objects.filter(pk=target.pk).exists())


class CropLayoutViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AdminFactory(username="admin", password="x", is_superuser=True)
        cls.location = LocationFactory(name="Site")
        cls.layout = CropLayoutFactory(location=cls.location, name="Visible")
        cls.archived = CropLayoutFactory(location=cls.location, name="Archived")
        cls.archived.archive()
        cls.species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        cls.variety = PlantVarietyFactory(name="Variety", species=cls.species)

    def setUp(self):
        self.client.force_login(self.user)

    def test_location_lists_only_visible_layouts(self):
        response = self.client.get(reverse("spaces:location_detail", args=(self.location.pk,)))

        self.assertContains(response, self.layout.get_absolute_url())
        self.assertNotContains(response, self.archived.get_absolute_url())

    def test_archived_layout_can_be_viewed_and_restored(self):
        CropFactory(layout=self.archived, variety=self.variety)

        response = self.client.get(self.archived.get_absolute_url())
        self.assertContains(response, self.variety.name)
        self.assertContains(response, "Archived")
        self.assertContains(response, self.archived.get_restore_url())
        self.assertNotContains(response, self.archived.get_update_url())
        self.assertNotContains(response, self.archived.get_archive_url())

        response = self.client.post(self.archived.get_restore_url())
        self.assertRedirects(response, self.archived.get_absolute_url())
        self.archived.refresh_from_db()
        self.assertFalse(self.archived.is_archived)

    def test_visible_layout_header_exposes_update_and_archive(self):
        response = self.client.get(self.layout.get_absolute_url())

        self.assertContains(response, self.layout.get_update_url())
        self.assertContains(response, self.layout.get_archive_url())
        self.assertNotContains(response, self.layout.get_restore_url())
        self.assertNotContains(response, ">Delete<", html=True)

    def test_layout_detail_requires_view_permission_and_archive_requires_change_permission(self):
        user = UserFactory(username="viewer", password="x")
        self.client.force_login(user)

        response = self.client.get(self.layout.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename="view_croplayout"))
        response = self.client.get(self.layout.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.layout.get_update_url())
        self.assertNotContains(response, self.layout.get_archive_url())

        response = self.client.get(self.archived.get_absolute_url())
        self.assertContains(response, "Archived")
        self.assertNotContains(response, self.archived.get_restore_url())

        archive_url = self.layout.get_archive_url()
        response = self.client.post(archive_url)
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename="change_croplayout"))
        response = self.client.post(archive_url)
        self.assertRedirects(response, self.layout.get_absolute_url())
        self.layout.refresh_from_db()
        self.assertTrue(self.layout.is_archived)

    def test_archive_requires_post_and_requested_lifecycle_state(self):
        response = self.client.get(self.layout.get_archive_url())
        self.assertEqual(response.status_code, 405)

        response = self.client.post(self.layout.get_archive_url())
        self.assertRedirects(response, self.layout.get_absolute_url())
        response = self.client.post(self.layout.get_archive_url())
        self.assertEqual(response.status_code, 404)

        response = self.client.post(self.layout.get_restore_url())
        self.assertRedirects(response, self.layout.get_absolute_url())
        response = self.client.post(self.layout.get_restore_url())
        self.assertEqual(response.status_code, 404)

    def test_archive_and_restore_htmx_requests_redirect_the_full_page(self):
        layout = CropLayoutFactory(location=self.location)

        response = self.client.post(layout.get_archive_url(), headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Redirect"], layout.get_absolute_url())

        response = self.client.post(layout.get_restore_url(), headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Redirect"], layout.get_absolute_url())

    def test_crop_reordering_rejects_crops_from_different_layouts(self):
        first_crop = CropFactory(layout=self.layout, variety=self.variety, order=0)
        other_layout = CropLayoutFactory(location=self.location, name="Other")
        second_crop = CropFactory(layout=other_layout, variety=self.variety, order=0)

        response = self.client.post(reverse("calculator:crop_sort"), {"order": [first_crop.pk, second_crop.pk]})

        self.assertEqual(response.status_code, 400)
        first_crop.refresh_from_db()
        second_crop.refresh_from_db()
        self.assertEqual(first_crop.order, 0)
        self.assertEqual(second_crop.order, 0)

    def test_crop_reordering_rejects_an_incomplete_layout(self):
        first_crop = CropFactory(layout=self.layout, variety=self.variety, order=0)
        second_crop = CropFactory(layout=self.layout, variety=self.variety, order=1)

        response = self.client.post(reverse("calculator:crop_sort"), {"order": [second_crop.pk]})

        self.assertEqual(response.status_code, 400)
        first_crop.refresh_from_db()
        second_crop.refresh_from_db()
        self.assertEqual(first_crop.order, 0)
        self.assertEqual(second_crop.order, 1)

    def test_crop_reordering_is_permission_protected(self):
        crop = CropFactory(layout=self.layout, variety=self.variety, order=0)
        user = UserFactory(username="viewer", password="x")
        user.user_permissions.add(Permission.objects.get(codename="view_croplayout"))
        self.client.force_login(user)

        response = self.client.post(reverse("calculator:crop_sort"), {"order": [crop.pk]})

        self.assertEqual(response.status_code, 403)

    def test_layout_update_persists_submitted_changes(self):
        response = self.client.post(
            reverse("calculator:layout_update", args=(self.layout.pk,)),
            {"name": "Renamed", "description": "Updated", "ncol": 3},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.layout.refresh_from_db()
        self.assertEqual(self.layout.name, "Renamed")

    def test_crop_creation_adds_crop_to_requested_layout(self):
        existing_crop = CropFactory(layout=self.layout, order=0)

        response = self.client.post(
            reverse("calculator:layout_crop_create", args=(self.layout.pk,)),
            {"species": self.species.pk, "variety": self.variety.pk, "notes": ""},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        created_crop = self.layout.crops.get(variety=self.variety)
        self.assertEqual(created_crop.order, existing_crop.order)

    def test_crop_update_allows_only_varieties_from_the_existing_species(self):
        crop = CropFactory(layout=self.layout, variety=self.variety)
        same_species_variety = PlantVarietyFactory(species=self.species)
        update_url = reverse("calculator:crop_update", args=(crop.pk,))

        response = self.client.post(update_url, {"variety": same_species_variety.pk, "notes": "Updated"})

        self.assertRedirects(response, crop.get_absolute_url())
        crop.refresh_from_db()
        self.assertEqual(crop.variety, same_species_variety)

        other_species = PlantSpeciesFactory(common_name="Rice", latin_name="Oryza sativa")
        other_species_variety = PlantVarietyFactory(species=other_species)
        response = self.client.post(update_url, {"variety": other_species_variety.pk, "notes": "Invalid"})

        self.assertEqual(response.status_code, 200)
        crop.refresh_from_db()
        self.assertEqual(crop.variety, same_species_variety)

    def test_fieldbook_creation_supports_htmx_and_form_submissions(self):
        create_url = reverse("calculator:fieldbook_create", args=(self.layout.pk,))
        requests = (
            ("HTMX book", {"HX-Request": "true"}, 200),
            ("Form book", {}, 302),
        )

        for name, headers, expected_status in requests:
            with self.subTest(headers=headers):
                response = self.client.post(create_url, {"name": name}, headers=headers)

                self.assertEqual(response.status_code, expected_status)
                self.assertTrue(self.layout.fieldbooks.filter(name=name).exists())


class FieldBookTargetDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AdminFactory(username="admin", password="x", is_superuser=True)
        cls.layout = CropLayoutFactory(name="Layout")
        cls.species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum",
            plant_type="herbaceous",
        )
        cls.variety = PlantVarietyFactory(name="Wheat variety", species=cls.species)
        cls.first_crop = CropFactory(layout=cls.layout, variety=cls.variety, order=0)
        cls.second_crop = CropFactory(layout=cls.layout, variety=cls.variety, order=1)
        cls.third_crop = CropFactory(layout=cls.layout, variety=cls.variety, order=2)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Book")
        cls.protocol = ProtocolFactory(name="Wheat protocol", plantspecies=cls.species)
        cls.observed_trait = TraitFactory(numeric_id=1, description="Height", protocol=cls.protocol)
        cls.unobserved_trait = TraitFactory(numeric_id=2, description="Colour", protocol=cls.protocol)
        cls.state = StateFactory(numeric_id=1, description="Tall", trait=cls.observed_trait)
        cls.parameter = ParameterFactory(code="weight", name="Weight")

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse("calculator:fieldbook_targets_delete", args=(self.fieldbook.pk,))

    def test_removes_only_unobserved_targets_from_selected_crops_and_cleans_empty_steps(self):
        selected_step = StepFactory(fieldbook=self.fieldbook, crop=self.first_crop, order=0)
        unselected_step = StepFactory(fieldbook=self.fieldbook, crop=self.second_crop, order=1)
        emptyable_step = StepFactory(fieldbook=self.fieldbook, crop=self.third_crop, order=2)
        observed_target = TraitTarget.objects.create(step=selected_step, trait=self.observed_trait)
        removable_trait_target = TraitTarget.objects.create(step=selected_step, trait=self.unobserved_trait)
        removable_parameter_target = ParameterTarget.objects.create(step=selected_step, parameter=self.parameter)
        observed_parameter_target = ParameterTarget.objects.create(step=unselected_step, parameter=self.parameter)
        unselected_target = TraitTarget.objects.create(step=unselected_step, trait=self.unobserved_trait)
        emptyable_target = TraitTarget.objects.create(step=emptyable_step, trait=self.unobserved_trait)
        TraitObservation.objects.create(
            crop=self.first_crop,
            step=selected_step,
            state=self.state,
            created_by=self.user,
        )
        ParameterObservation.objects.create(
            crop=self.second_crop,
            step=unselected_step,
            parameter=self.parameter,
            parameter_value=1,
            created_by=self.user,
        )

        response = self.client.post(self.url, {"selection": [self.first_crop.pk]}, follow=True)

        self.assertRedirects(response, self.fieldbook.get_absolute_url())
        self.assertTrue(TraitTarget.objects.filter(pk=observed_target.pk).exists())
        self.assertFalse(TraitTarget.objects.filter(pk=removable_trait_target.pk).exists())
        self.assertFalse(ParameterTarget.objects.filter(pk=removable_parameter_target.pk).exists())
        self.assertTrue(TraitTarget.objects.filter(pk=unselected_target.pk).exists())
        self.assertTrue(Step.objects.filter(pk=selected_step.pk).exists())
        self.assertTrue(Step.objects.filter(pk=unselected_step.pk).exists())
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn("Some targets were not removed because they have already been observed.", messages)

        response = self.client.post(self.url, {"selection": [self.second_crop.pk, self.third_crop.pk]})

        self.assertRedirects(response, self.fieldbook.get_absolute_url())
        self.assertTrue(ParameterTarget.objects.filter(pk=observed_parameter_target.pk).exists())
        self.assertFalse(TraitTarget.objects.filter(pk=unselected_target.pk).exists())
        self.assertFalse(TraitTarget.objects.filter(pk=emptyable_target.pk).exists())
        self.assertTrue(Step.objects.filter(pk=unselected_step.pk).exists())
        self.assertFalse(Step.objects.filter(pk=emptyable_step.pk).exists())

    def test_clears_display_only_after_the_last_matching_target_is_removed(self):
        first_step = StepFactory(fieldbook=self.fieldbook, crop=self.first_crop, order=0)
        second_step = StepFactory(fieldbook=self.fieldbook, crop=self.second_crop, order=1)
        TraitTarget.objects.create(step=first_step, trait=self.unobserved_trait)
        TraitTarget.objects.create(step=second_step, trait=self.unobserved_trait)
        self.fieldbook.set_display_config("trait", self.unobserved_trait.pk)
        self.fieldbook.save()

        self.client.post(self.url, {"selection": [self.first_crop.pk]})
        self.fieldbook.refresh_from_db()
        self.assertIsNotNone(self.fieldbook.display_config)

        self.client.post(self.url, {"selection": [self.second_crop.pk]})
        self.fieldbook.refresh_from_db()
        self.assertIsNone(self.fieldbook.display_config)


class ZigzagPairTests(TestCase):
    def test_plot_order_is_relative_to_each_blocks_direction_of_travel(self):
        self.assertEqual(
            list(generate_zigzag_pairs(4, 2, block_width=2, start_corner="SE")),
            [
                (3, 2),
                (4, 2),
                (3, 1),
                (4, 1),
                (2, 1),
                (1, 1),
                (2, 2),
                (1, 2),
            ],
        )


class FieldBookStepOrderViewTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="admin", password="x", is_superuser=True)
        self.client.force_login(self.user)
        self.layout = CropLayoutFactory(ncol=3)
        self.fieldbook = FieldBookFactory(layout=self.layout)
        self.crops = [CropFactory(layout=self.layout, order=order) for order in range(7)]
        self.steps = [
            StepFactory(fieldbook=self.fieldbook, crop=crop, order=10 + order)
            for order, crop in enumerate(self.crops)
            if order != 4
        ]
        self.url = reverse("calculator:fieldbook_update_step_order", args=(self.fieldbook.pk,))

    def test_pattern_ordering_skips_empty_plots_in_incomplete_final_row(self):
        response = self.client.post(
            self.url,
            {"start_corner": "NW", "block_width": 2, "plot_order": "right_first"},
        )

        self.assertRedirects(response, self.fieldbook.get_absolute_url())
        ordered_crop_ids = list(
            Step.objects.filter(fieldbook=self.fieldbook).order_by("order").values_list("crop_id", flat=True)
        )
        self.assertEqual(
            ordered_crop_ids,
            [
                self.crops[0].pk,
                self.crops[1].pk,
                self.crops[3].pk,
                self.crops[6].pk,
                self.crops[5].pk,
                self.crops[2].pk,
            ],
        )
        self.assertEqual(
            list(Step.objects.filter(fieldbook=self.fieldbook).order_by("order").values_list("order", flat=True)),
            list(range(6)),
        )


class ArchivedLayoutReadOnlyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AdminFactory(username="archive-admin", password="x", is_superuser=True)
        cls.layout = CropLayoutFactory(name="Archived layout", ncol=2)
        cls.species = PlantSpeciesFactory(
            common_name="Wheat",
            latin_name="Triticum aestivum",
            plant_type="herbaceous",
        )
        cls.variety = PlantVarietyFactory(name="Archive variety", species=cls.species)
        cls.other_variety = PlantVarietyFactory(name="Other variety", species=cls.species)
        cls.first_crop = CropFactory(layout=cls.layout, variety=cls.variety, order=0, notes="Original")
        cls.second_crop = CropFactory(layout=cls.layout, variety=cls.other_variety, order=1)
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Archive book")
        cls.step = StepFactory(fieldbook=cls.fieldbook, crop=cls.first_crop, order=0)
        cls.protocol = ProtocolFactory(name="Archive protocol", plantspecies=cls.species)
        cls.trait = TraitFactory(numeric_id=1, description="Height", protocol=cls.protocol)
        cls.state = StateFactory(numeric_id=1, description="Tall", trait=cls.trait)
        cls.parameter = ParameterFactory(code="archive-weight", name="Weight")
        cls.trait_target = TraitTarget.objects.create(step=cls.step, trait=cls.trait)
        cls.parameter_target = ParameterTarget.objects.create(step=cls.step, parameter=cls.parameter)
        cls.trait_observation = TraitObservation.objects.create(
            crop=cls.first_crop,
            step=cls.step,
            state=cls.state,
            created_by=cls.user,
        )
        cls.parameter_observation = ParameterObservation.objects.create(
            crop=cls.first_crop,
            step=cls.step,
            parameter=cls.parameter,
            parameter_value=1,
            created_by=cls.user,
        )
        cls.layout.archive()

    def setUp(self):
        self.client.force_login(self.user)

    def test_archived_layout_blocks_direct_crop_and_fieldbook_mutations(self):
        requests = (
            ("calculator:layout_update", (self.layout.pk,), {"name": "Changed", "ncol": 3}),
            ("calculator:layout_crop_create", (self.layout.pk,), {}),
            ("calculator:fieldbook_create", (self.layout.pk,), {"name": "New book"}),
            ("calculator:layout_management_create", (self.layout.pk,), {}),
            ("calculator:crop_update", (self.first_crop.pk,), {"variety": self.variety.pk, "notes": "Changed"}),
            ("calculator:crop-delete", (self.second_crop.pk,), {}),
            ("calculator:crop_sort", (), {"order": [self.second_crop.pk, self.first_crop.pk]}),
        )

        for view_name, args, payload in requests:
            with self.subTest(view_name=view_name):
                response = self.client.post(reverse(view_name, args=args), payload)
                self.assertEqual(response.status_code, 404)

        self.layout.refresh_from_db()
        self.first_crop.refresh_from_db()
        self.second_crop.refresh_from_db()
        self.assertEqual(self.layout.name, "Archived layout")
        self.assertEqual(self.first_crop.notes, "Original")
        self.assertEqual((self.first_crop.order, self.second_crop.order), (0, 1))
        self.assertTrue(self.layout.crops.filter(pk=self.second_crop.pk).exists())
        self.assertEqual(self.layout.fieldbooks.count(), 1)
        self.assertFalse(self.layout.managements.exists())

    def test_archived_layout_blocks_target_and_observation_mutations(self):
        requests = (
            ("calculator:fieldbook_update_step_order", (self.fieldbook.pk,), {}),
            ("calculator:fieldbook_targets_delete", (self.fieldbook.pk,), {"selection": [self.first_crop.pk]}),
            ("calculator:trait_target_create", (self.fieldbook.pk,), {"selection": [self.first_crop.pk]}),
            ("calculator:parameter_target_create", (self.fieldbook.pk,), {"selection": [self.first_crop.pk]}),
            ("calculator:trait_target_delete", (self.trait_target.pk,), {}),
            ("calculator:parameter_target_delete", (self.parameter_target.pk,), {}),
            ("calculator:observation_expression_create", (self.first_crop.pk,), {}),
            ("calculator:observation_parameter_create", (self.first_crop.pk,), {}),
            ("calculator:trait_observation_update", (self.trait_observation.pk,), {}),
            ("calculator:trait_observation_delete", (self.trait_observation.pk,), {}),
            ("calculator:parameter_observation_update", (self.parameter_observation.pk,), {}),
            ("calculator:parameter_observation_delete", (self.parameter_observation.pk,), {}),
            ("calculator:trait_observation_in_step_create", (self.step.pk,), {}),
            ("calculator:parameter_observation_in_step_create", (self.step.pk,), {}),
        )

        for view_name, args, payload in requests:
            with self.subTest(view_name=view_name):
                response = self.client.post(reverse(view_name, args=args), payload)
                self.assertEqual(response.status_code, 404)

        self.assertTrue(TraitTarget.objects.filter(pk=self.trait_target.pk).exists())
        self.assertTrue(ParameterTarget.objects.filter(pk=self.parameter_target.pk).exists())
        self.assertTrue(TraitObservation.objects.filter(pk=self.trait_observation.pk).exists())
        self.assertTrue(ParameterObservation.objects.filter(pk=self.parameter_observation.pk).exists())

    def test_archived_pages_show_records_without_mutation_controls(self):
        pages_and_hidden_urls = (
            (
                self.layout.get_absolute_url(),
                (
                    reverse("calculator:layout_crop_create", args=(self.layout.pk,)),
                    reverse("calculator:fieldbook_create", args=(self.layout.pk,)),
                    reverse("calculator:layout_management_create", args=(self.layout.pk,)),
                    reverse("calculator:crop_sort"),
                ),
            ),
            (
                self.first_crop.get_absolute_url(),
                (
                    self.first_crop.get_update_url(),
                    self.first_crop.get_delete_url(),
                    reverse("calculator:observation_expression_create", args=(self.first_crop.pk,)),
                    reverse("calculator:observation_parameter_create", args=(self.first_crop.pk,)),
                    reverse("calculator:trait_observation_update", args=(self.trait_observation.pk,)),
                    reverse("calculator:parameter_observation_update", args=(self.parameter_observation.pk,)),
                ),
            ),
            (
                self.fieldbook.get_absolute_url(),
                (
                    reverse("calculator:fieldbook_update_step_order", args=(self.fieldbook.pk,)),
                    reverse("calculator:trait_target_create", args=(self.fieldbook.pk,)),
                    reverse("calculator:parameter_target_create", args=(self.fieldbook.pk,)),
                ),
            ),
            (
                self.step.get_absolute_url(),
                (
                    reverse("calculator:trait_observation_in_step_create", args=(self.step.pk,)),
                    reverse("calculator:parameter_observation_in_step_create", args=(self.step.pk,)),
                    reverse("calculator:trait_target_delete", args=(self.trait_target.pk,)),
                    reverse("calculator:parameter_target_delete", args=(self.parameter_target.pk,)),
                ),
            ),
        )

        for page_url, hidden_urls in pages_and_hidden_urls:
            with self.subTest(page_url=page_url):
                response = self.client.get(page_url)
                self.assertEqual(response.status_code, 200)
                for hidden_url in hidden_urls:
                    self.assertNotContains(response, hidden_url)

        self.assertContains(self.client.get(self.first_crop.get_absolute_url()), self.state.description)
        self.assertContains(self.client.get(self.step.get_absolute_url()), "Recorded observations")

    def test_archived_fieldbook_allows_display_config_changes(self):
        display_url = reverse("calculator:fieldbook_detail_display", args=(self.fieldbook.pk,))

        response = self.client.get(self.fieldbook.get_absolute_url())
        self.assertContains(response, display_url)

        response = self.client.post(display_url, {"display_config": f"trait:{self.trait.pk}:value"})
        self.assertRedirects(response, self.fieldbook.get_absolute_url())

        self.fieldbook.refresh_from_db()
        self.assertEqual(
            self.fieldbook.display_config,
            {"model": "trait", "id": self.trait.pk, "field": "value"},
        )
        self.assertContains(self.client.get(self.fieldbook.get_absolute_url()), self.state.description)

    def test_restoration_reenables_direct_and_nested_mutations(self):
        response = self.client.post(self.layout.get_restore_url())
        self.assertRedirects(response, self.layout.get_absolute_url())

        response = self.client.post(
            reverse("calculator:layout_update", args=(self.layout.pk,)),
            {"name": "Restored layout", "description": "", "ncol": 2},
        )
        self.assertRedirects(response, self.layout.get_absolute_url())
        response = self.client.post(
            reverse("calculator:crop_update", args=(self.first_crop.pk,)),
            {"variety": self.variety.pk, "notes": "Restored mutation"},
        )
        self.assertRedirects(response, self.first_crop.get_absolute_url())

        self.layout.refresh_from_db()
        self.first_crop.refresh_from_db()
        self.assertEqual(self.layout.name, "Restored layout")
        self.assertEqual(self.first_crop.notes, "Restored mutation")


class CropLayoutDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = LocationFactory(name="Delete site")
        cls.user = UserFactory(username="layout-deleter", password="x")
        cls.user.user_permissions.add(
            Permission.objects.get(codename="delete_croplayout"),
            Permission.objects.get(codename="view_croplayout"),
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_success_redirects_to_list_and_cascades_managements(self):
        layout = CropLayoutFactory(location=self.location)
        management_type = ManagementType.objects.create(code="water", name="Water")
        Management.objects.create(type=management_type, date=date(2026, 1, 1), layout=layout)
        delete_url = reverse("calculator:layout_delete", args=(layout.pk,))

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("calculator:croplayout_list"))
        self.assertFalse(type(layout).objects.filter(pk=layout.pk).exists())
        self.assertFalse(Management.objects.filter(layout_id=layout.pk).exists())

    def test_protected_layout_remains_and_redirects_to_detail_with_explanation(self):
        layout = CropLayoutFactory(location=self.location)
        CropFactory(layout=layout)
        delete_url = reverse("calculator:layout_delete", args=(layout.pk,))

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, layout.get_absolute_url())
        self.assertTrue(type(layout).objects.filter(pk=layout.pk).exists())
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn(layout.cant_delete_msg, messages)

    def test_direct_post_requires_delete_permission(self):
        layout = CropLayoutFactory(location=self.location)
        user = UserFactory(username="layout-viewer", password="x")
        user.user_permissions.add(Permission.objects.get(codename="view_croplayout"))
        self.client.force_login(user)

        response = self.client.post(reverse("calculator:layout_delete", args=(layout.pk,)))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(type(layout).objects.filter(pk=layout.pk).exists())

    def test_htmx_uses_outcome_specific_full_page_redirects(self):
        deletable_layout = CropLayoutFactory(location=self.location)
        protected_layout = CropLayoutFactory(location=self.location)
        FieldBookFactory(layout=protected_layout)

        response = self.client.post(
            reverse("calculator:layout_delete", args=(deletable_layout.pk,)),
            headers={"HX-Request": "true"},
        )
        self.assertEqual(response.headers["HX-Redirect"], reverse("calculator:croplayout_list"))

        response = self.client.post(
            reverse("calculator:layout_delete", args=(protected_layout.pk,)),
            headers={"HX-Request": "true"},
        )
        self.assertEqual(response.headers["HX-Redirect"], protected_layout.get_absolute_url())

    def test_protected_layout_delete_action_is_disabled(self):
        layout = CropLayoutFactory(location=self.location)
        CropFactory(layout=layout)
        self.user.user_permissions.add(Permission.objects.get(codename="view_croplayout"))

        response = self.client.get(layout.get_absolute_url())

        self.assertContains(response, 'class="dropdown-item disabled"')
        self.assertContains(response, layout.cant_delete_msg)
        self.assertNotContains(response, f'hx-get="{reverse("calculator:layout_delete", args=(layout.pk,))}"')
