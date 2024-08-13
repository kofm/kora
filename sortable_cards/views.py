from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.db import transaction


class SortableView(View):
    model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.model is None:
            raise Http404("A model must be provided")

    def post(self, request, *args, **kwargs):

        try: 
            sorted_ids = [int(pk) for pk in request.POST.getlist("order")]
        except ValueError:
            return HttpResponseBadRequest("Invalid object ids provided.", content_type="text/plain")

        queryset = self.model.objects.filter(pk__in=sorted_ids)

        if len(sorted_ids) != queryset.count():
            return HttpResponseBadRequest("Invalid object ids provided.")

        sorted_mapping = {pk: order for order, pk in enumerate(sorted_ids)}

        with transaction.atomic():
            for object in queryset:
                object.order = sorted_mapping[object.pk]

            self.model.objects.bulk_update(queryset, ["order"])

        return JsonResponse({"status": "success"})
