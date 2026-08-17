from datetime import datetime
from typing import Any

from rest_framework import serializers
from rest_framework import serializers as sr

from restapi.serializers.generic import parse_semicolon_string


class ExcelSafeDateField(serializers.DateField):
    def to_internal_value(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return super().to_internal_value(value)


class MappedPrimaryKeyRelatedField(sr.Field):
    default_error_messages = {
        "does_not_exist": 'Invalid pk "{pk_value}" - object does not exist.',
        "incorrect_type": "Incorrect type. Expected pk value, received {data_type}.",
    }

    def __init__(self, mapping_key, pk_field=None, **kwargs):
        self.mapping_key = mapping_key
        self.pk_field = pk_field
        super().__init__(**kwargs)

    def get_mapping(self):
        return self.context.get(self.mapping_key, {})

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)

        try:
            if isinstance(data, bool):
                raise TypeError
            return self.get_mapping()[data]
        except KeyError:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def to_representation(self, value):
        return value.pk


class CSV2ListQueryField(sr.ListField):
    """A ListField variant for semicolon-separated string fields that
    returns tuple(value,) to be used with QueryField child

    The mappings are list[dict[tuple, type[Model]]]; therefore, to
    access the mapping, `to_internal_value` should return a list of tuples.

    """

    def __init__(self, *, mapping_key, column_mapping, **kwargs):
        child = QueryField(mapping_key=mapping_key, column_mapping=column_mapping)
        super().__init__(child=child, **kwargs)

    def to_internal_value(self, data: Any) -> list[tuple]:
        if isinstance(data, str):
            data = [(val,) for val in parse_semicolon_string(data)]
        return super().to_internal_value(data)


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
