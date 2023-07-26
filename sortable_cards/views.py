from django.http import Http404
from django.http.response import HttpResponse
from django.views import View


class SortableView(View):
    model = None

    def post(self, request, *args, **kwargs):
        if self.model is None:
            raise Http404("A model must be provided")

        sorted_ids = [int(pk) for pk in request.POST.getlist("order")]

        queryset = self.model.objects.filter(pk__in=sorted_ids)

        sorted_mapping = {pk: order for order, pk in enumerate(sorted_ids)}

        for object in queryset:
            object.order = sorted_mapping[object.pk]

        self.model.objects.bulk_update(
            queryset,
            [
                "order",
            ],
        )

        return HttpResponse()
