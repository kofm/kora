from django.utils.functional import cached_property


class ModelIsDeletableMixin:
    @cached_property
    def is_deletable(self):
        for field in self._meta.get_fields():
            try:
                if field.on_delete.__name__ not in ["PROTECT", "RESTRICT"]:
                    continue
                related_object = field.related_model.objects.filter(**{field.field.name: self})
                if related_object.exists():
                    return False
            except AttributeError:
                pass
        return True
