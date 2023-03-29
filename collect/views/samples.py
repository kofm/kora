from django.http import HttpResponseBadRequest
from django.http.response import HttpResponse
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.template.response import TemplateResponse

from django.db.models.functions import Cast, Concat
from django.db.models import Value

from collect.models import SeedSample, StoragePosition
from register.models import PlantVarietyName
from collect.models import SeedSample

from django.db.models import IntegerField
from collect.forms import (
    CartSelectForm,
    GerminabilityForm,
    SampleWeightForm,
    SeedSampleForm,
)

from django_tables2 import RequestConfig
from collect.tables import SeedSampleDuplicatesTable, SeedSampleTable

from collect.filters import SeedSampleFilter


def seedsample_list(request):
    context = {}

    filter = SeedSampleFilter(request.GET)
    table = SeedSampleTable(filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    context.update(
        {
            "table": table,
            "filter": filter,
        }
    )

    if request.user.is_authenticated:
        cart = request.user.carts.active() or None
        context["cart"] = cart
        cart_select_form = CartSelectForm(initial={"cart": cart}, user=request.user)
        context["cart_select_form"] = cart_select_form

    template_file = "collect/seedsample_list.html"

    if request.htmx:
        template_file = "collect/partials/seedsample_table.html"

    return TemplateResponse(request, template_file, context)


@require_POST
@login_required
def cart_change_htmx(request):
    form = CartSelectForm(request.POST, user=request.user)
    if form.is_valid():
        cart = form.save()
        return TemplateResponse(request, "collect/partials/cart_offcanvas.html", {"cart": cart})
    else:
        return HttpResponseBadRequest()


def seedsample_detail(request, pk):
    context = {}
    seedsample = get_object_or_404(SeedSample, pk=pk)
    context["seedsample"] = seedsample
    context["seedsample_duplicates_table"] = SeedSampleDuplicatesTable(
        seedsample.duplicate_samples
    )
    return TemplateResponse(request, "collect/seedsample_detail.html", context)


class SeedSampleCreateView(CreateView):
    form_class = SeedSampleForm
    model = SeedSample

    def form_valid(self, form):
        response = super(SeedSampleCreateView, self).form_valid(form)
        weight_form = SampleWeightForm(self.request.POST)
        new_weight = weight_form.save(commit=False)
        new_weight.seedsample = self.object
        new_weight.save()
        if self.request.POST.get("germinability"):
            germinability_form = GerminabilityForm(self.request.POST)
            new_germinability = germinability_form.save(commit=False)
            new_germinability.seedsample = self.object
            new_germinability.save()
        return response

    def get_form(self):
        form = super(SeedSampleCreateView, self).get_form()
        samples_id = SeedSample.objects.all().values_list("sample_id", flat=True)
        sample_id = max(samples_id) + 1 if samples_id else 1
        form.fields["sample_id"].initial = sample_id
        form.fields["growing_season"].initial = now().year - 1
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weight_form"] = SampleWeightForm()
        context["germinability_form"] = GerminabilityForm(initial={"after_days": 7})
        context["varieties"] = list(
            PlantVarietyName.objects.values("variety__id", "name")
        )
        context["positions"] = list(
            StoragePosition.objects.filter(seedsample__isnull=True)
            .annotate(
                position_name=Concat("storage__name", Value("-"), "name"),
                posn=Cast("name", output_field=IntegerField()),
            )
            .order_by("storage__name", "posn")
            .values("pk", "position_name")
        )
        return context
