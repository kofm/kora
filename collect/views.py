from django.db.models.aggregates import Max
from django.utils.timezone import now
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collect.forms import GerminabilityForm, SampleWeightForm, SeedSampleForm

from collect.models import (
    Germinability,
    SampleWeight,
    SeedSample,
    Storage,
    StoragePosition,
)
from collect.serializers import (
    GerminabilitySerializer,
    SampleWeightSerializer,
)
from register.models import PlantVariety


class StorageCreateView(CreateView):
    model = Storage
    fields = [
        "name",
    ]


class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search and search != '':
            if len(search) < 2:
                queryset = SeedSample.objects.filter(variety__names__name__istartswith=search)
            else:
                queryset = SeedSample.objects.filter(variety__names__name__unaccent__lower__trigram_similar=search)
        else:
            queryset = SeedSample.objects.all()
        return queryset

    def get_storages(self):
        queryset = Storage.objects.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("storage_page")
        storages = paginator.get_page(page)
        return storages


class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = "sample"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.filter(
            storageposition__seedsample__isnull=True
        )
        context["variety_list"] = PlantVariety.objects.all()
        context["sample_form"] = SeedSampleForm(instance=self.object)
        return context


class SeedSampleCreateView(CreateView):
    form_class = SeedSampleForm
    model = SeedSample

    def form_valid(self, form):
        response = super(SeedSampleCreateView, self).form_valid(form)
        weight_form=SampleWeightForm(self.request.POST)
        new_weight = weight_form.save(commit=False)
        new_weight.seedsample = self.object
        new_weight.save()
        if self.request.POST.get('germinability'):
            germinability_form = GerminabilityForm(self.request.POST)
            new_germinability = germinability_form.save(commit=False)
            new_germinability.seedsample = self.object
            new_germinability.save()
        return response

    def get_form(self):
        form = super(SeedSampleCreateView, self).get_form()
        samples_id = SeedSample.objects.all().values_list('sample_id', flat = True)
        sample_id = max(samples_id) + 1 if samples_id else 1
        form.fields["sample_id"].initial = sample_id
        form.fields["growing_season"].initial = now().year - 1
        form.fields["position"].initial = StoragePosition.objects.filter(seedsample__isnull=True).first()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weight_form'] = SampleWeightForm()
        context['germinability_form'] = GerminabilityForm(initial={'after_days': 7})
        context['varieties'] = list(PlantVariety.objects.values('pk', 'names__name'))
        return context

    def get_success_url(self):
        if "btn-another" in self.request.POST:
            return reverse("collect:seedsample-create")
        return super().get_success_url()


class SeedSampleUpdateView(UpdateView):
    form_class = SeedSampleForm
    model = SeedSample


class SeedSampleDeleteView(DeleteView):
    model = SeedSample
    success_url = reverse_lazy('collect:seedsamples-list')

class StorageListView(ListView):
    model = Storage
    paginate_by = 10


@api_view(["GET", "POST"])
def germinability(request):
    if request.method == "GET":
        snippets = Germinability.objects.all()
        serializer = GerminabilitySerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = GerminabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def sample_weight(request):
    if request.method == "GET":
        snippets = SampleWeight.objects.all()
        serializer = SampleWeightSerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = SampleWeightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
