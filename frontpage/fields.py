from django import forms
from django.core.exceptions import ValidationError


class RemoteModelIdFieldMixin:
    model = None
    queryset = None

    default_error_messages = {
        "invalid": "Enter a valid ID.",
        "invalid_choice": "Object does not exist: %(ids)s",
    }

    def __init__(self, *args, model=None, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if queryset is not None:
            self.queryset = queryset
        elif model is not None:
            self.queryset = model._default_manager.all()
        elif self.queryset is None and self.model is not None:
            self.queryset = self.model._default_manager.all()

        if self.queryset is None:
            raise ValueError(f"{self.__class__.__name__} requires either model or queryset.")

    def validate_ids_exist(self, ids):
        existing = set(self.queryset.filter(pk__in=ids).values_list("pk", flat=True))

        missing = set(ids) - existing

        if missing:
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"ids": sorted(missing)},
            )


class RemoteModelChoiceField(RemoteModelIdFieldMixin, forms.Field):
    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            return int(value)
        except (TypeError, ValueError) as err:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
            ) from err

    def validate(self, value):
        super().validate(value)

        if value is None:
            return

        self.validate_ids_exist([value])


class RemoteModelMultipleChoiceField(RemoteModelIdFieldMixin, forms.Field):
    def to_python(self, value):
        if value in self.empty_values:
            return []

        try:
            return [int(v) for v in value]
        except (TypeError, ValueError) as err:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
            ) from err

    def validate(self, value):
        super().validate(value)

        if not value:
            return

        self.validate_ids_exist(value)
