from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models import Model
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View


class SortableView(View):
    model: None | type[Model] = None
    order_field: str = "order"

    def _parse_ids(self, request):
        try:
            return [int(pk) for pk in request.POST.getlist("order")]
        except ValueError as exc:
            raise ValueError("Invalid object ids provided.") from exc

    def validate_objects(self, objs):
        return None

    def post(self, request):
        if self.model is None:
            exc = "A model must be provided."
            raise ImproperlyConfigured(exc)
        if not issubclass(self.model, Model):
            exc = "Property 'model' should be a Django ORM Model."
            raise ImproperlyConfigured(exc)
        if not hasattr(self.model, self.order_field):
            exc = f"The model must have an {self.order_field} field."
            raise ImproperlyConfigured(exc)

        try:
            sorted_ids = self._parse_ids(request)
        except ValueError as exc:
            return HttpResponseBadRequest(exc, content_type="text/plain")

        if not sorted_ids:
            return HttpResponseBadRequest("Empty order list.")

        with transaction.atomic():
            objs = list(self.model.objects.filter(pk__in=sorted_ids))

            if len(sorted_ids) != len(objs):
                return HttpResponseBadRequest("Invalid object ids provided.")

            validation_response = self.validate_objects(objs)
            if validation_response is not None:
                return validation_response

            mapping = {pk: order for order, pk in enumerate(sorted_ids)}

            for obj in objs:
                setattr(obj, self.order_field, mapping[obj.pk])

            self.model.objects.bulk_update(objs, [self.order_field])

        return HttpResponse()
