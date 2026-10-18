from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from calculator.factories import CropFactory
from calculator.models import CropParameter, ParameterObservation
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory
from parameters.filters import VarietalParameterFilter
from parameters.models import VarietalParameter
from parameters.values import VALUE_FIELDS


class TypedValueTests(TestCase):
    def test_reference_crop_and_observation_values_share_type_rules(self):
        crop = CropFactory()
        user = UserFactory()
        for kind, value in (
            ("boolean", False),
            ("integer", 0),
            ("decimal", Decimal("0.0000000001")),
            ("date", date(2026, 5, 20)),
            ("text", "Early maturity"),
        ):
            parameter = ParameterFactory(type=kind)
            for Model, context in (
                (VarietalParameter, {"variety": crop.variety}),
                (CropParameter, {"crop": crop}),
                (ParameterObservation, {"crop": crop, "created_by": user}),
            ):
                with self.subTest(kind=kind, model=Model.__name__):
                    record = Model.objects.create(parameter=parameter, **context, **{f"value_{kind}": value})
                    record.refresh_from_db()
                    self.assertEqual(record.value, value)
                    other_field = "value_text" if kind != "text" else "value_integer"
                    setattr(record, other_field, "extra" if kind != "text" else 1)
                    with self.assertRaises(ValidationError):
                        record.save()
                    for field in VALUE_FIELDS:
                        setattr(record, field, None)
                    setattr(record, other_field, "wrong type" if kind != "text" else 1)
                    with self.assertRaises(ValidationError):
                        record.save()

    def test_existing_records_cannot_be_reassigned_but_values_remain_editable(self):
        crop = CropFactory()
        parameter = ParameterFactory(type="integer")
        other = ParameterFactory(type="integer")
        for Model, context in (
            (VarietalParameter, {"variety": crop.variety}),
            (CropParameter, {"crop": crop}),
            (ParameterObservation, {"crop": crop, "created_by": UserFactory()}),
        ):
            with self.subTest(model=Model.__name__):
                record = Model.objects.create(parameter=parameter, value_integer=1, **context)
                record.value_integer = 2
                record.save()
                record.parameter = other
                with self.assertRaisesMessage(ValidationError, "Parameter cannot be changed after creation."):
                    record.save()
                record.refresh_from_db()
                self.assertEqual(record.parameter_id, parameter.pk)
                self.assertEqual(record.value_integer, 2)

    def test_numeric_ranges_do_not_truncate_fractional_bounds_for_integers(self):
        crop = CropFactory()
        integer = ParameterFactory(type="integer")
        decimal = ParameterFactory(type="decimal")
        VarietalParameter.objects.create(variety=crop.variety, parameter=integer, value_integer=2)
        included_integer = VarietalParameter.objects.create(variety=crop.variety, parameter=integer, value_integer=3)
        included_decimal = VarietalParameter.objects.create(
            variety=crop.variety, parameter=decimal, value_decimal=Decimal("2.5")
        )
        filtered = VarietalParameterFilter({"value_min": "2.5", "value_max": "3.5"}).qs
        self.assertCountEqual(filtered, [included_integer, included_decimal])
        self.assertCountEqual(VarietalParameterFilter({"value": "2.5"}).qs, [included_decimal])

    def test_parameter_type_is_immutable_even_without_values(self):
        parameter = ParameterFactory(type="decimal")
        parameter.type = "date"
        with self.assertRaisesMessage(ValidationError, "Parameter type cannot be changed"):
            parameter.save()
