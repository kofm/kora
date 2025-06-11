from django.db.models import Model
from rest_framework import serializers as sr


class MappedPrimaryKeyRelatedField(sr.PrimaryKeyRelatedField):
    """A PrimaryKeyRelatedField that uses a mapping for faster lookups."""

    def __init__(self, mapping_key, **kwargs):
        self.mapping_key = mapping_key
        super().__init__(**kwargs)

    def get_queryset(self) -> dict[int, type[Model]]:
        return self.context.get(self.mapping_key, {})

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        mapping = self.get_queryset()
        try:
            if isinstance(data, bool):
                raise TypeError
            return mapping[data]
        except KeyError:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)


class CSV2ListMappedPrimaryKeyRelatedField(sr.ListField):
    """A ListField variant for semi-colon separated fields that returna a list of ints

    This allows the input to have a csv2 field like `78; 12; 54` to represent m2m relationships"""

    def __init__(self, *, mapping_key, **kwargs):
        child = MappedPrimaryKeyRelatedField(mapping_key=mapping_key)
        super().__init__(child=child, **kwargs)

    def to_internal_value(self, raw: str) -> list[int]:
        value = []
        for val in raw.split(";"):
            val = val.strip()
            if not val:
                continue
            value.append(int(val))
        return super().to_internal_value(value)


class CSV2ListQueryField(sr.ListField):
    """A list query field for semi-colon separated fields that returns tuple(value,) to be used with QueryField child

    The mappings are list[dict[tuple, type[Model]]]; therefore, to
    access the mapping, `to_internal_value` should return a list of tuples.

    """

    def __init__(self, *, mapping_key, column_mapping, **kwargs):
        child = QueryField(mapping_key=mapping_key, column_mapping=column_mapping)
        super().__init__(child=child, **kwargs)

    def to_internal_value(self, raw: str) -> list[tuple]:
        value = []
        for val in raw.split(";"):
            val = val.strip()
            if not val:
                continue
            value.append((val,))
        return super().to_internal_value(value)


class QueryField(sr.Field):
    """Retrieve a RelatedModel using a query instead of its Primary Key."""

    default_error_messages = {
        "missing": "{columns} Values do not match any entry in the database",
    }

    def __init__(self, *args, mapping_key: str, column_mapping: dict, **kwargs) -> None:
        self.mapping_key = mapping_key
        self.column_mapping = column_mapping
        super().__init__(**kwargs)

    def to_representation(self, value):
        return value

    def get_value(self, dictionary):
        if not all(col in dictionary for col in self.column_mapping):
            return sr.empty
        return tuple(dictionary.get(col) for col in self.column_mapping)

    def to_internal_value(self, data):
        mapping = self.context.get(self.mapping_key, {})
        if data in mapping:
            return mapping[data]

        if self.required:
            self.fail(
                "missing",
                columns=", ".join(self.column_mapping),
            )

        return None
