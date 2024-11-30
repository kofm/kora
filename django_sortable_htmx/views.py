from typing import Generic, TypeVar

from django.db import transaction
from django.db.models import Model
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views import View

T = TypeVar("T", bound=Model)


class SortableView(View, Generic[T]):
    model: None | type[T] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.model is None:
            e = "A model must be provided."
            raise Http404(e)
        if not issubclass(self.model, Model):
            e = "Property 'model' should be a Django ORM Model."
            raise Http404(e)
        if not hasattr(self.model, "order"):
            e = "The model must have an 'order' field."
            raise Http404(e)

    def post(self, request):
        try:
            sorted_ids = [int(pk) for pk in request.POST.getlist("order")]
        except ValueError:
            return HttpResponseBadRequest("Invalid object ids provided.", content_type="text/plain")

        queryset = self.model.objects.filter(pk__in=sorted_ids)

        if len(sorted_ids) != queryset.count():
            return HttpResponseBadRequest("Invalid object ids provided.")

        sorted_mapping = {pk: order for order, pk in enumerate(sorted_ids)}

        with transaction.atomic():
            for instance in queryset:
                instance.order = sorted_mapping[instance.pk]

            self.model.objects.bulk_update(queryset, ["order"])

        return JsonResponse({"status": "success"})
