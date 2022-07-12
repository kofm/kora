from crispy_forms.helper import TEMPLATE_PACK
from django.db.models.expressions import F
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from describe.forms import DescriptionFilterFormSet, ExpressionForm, TraitFormSet
from register.utils import paged_object_list_context

from .models import Description, Expression, Protocol, State, Trait


class DescriptionsList(ListView):
    model = Description
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_descriptions"] = "active"
        protocol = Protocol.objects.get(name="TP16/3")
        traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))
        context["form"] = DescriptionFilterFormSet(initial=traits)
        return context


def description_list(request):
    context = {}
    print(request.POST)
    protocol = Protocol.objects.get(name="TP16/3")
    traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))
    formset = DescriptionFilterFormSet(request.POST, initial=traits)
    context = dict()
    d = Description.objects.all().prefetch_related("expressions")
    if formset.is_valid():
        for form in formset:
            if form.cleaned_data["state_of_expression"]:
                print(form.cleaned_data["state_of_expression"])
                d = d.filter(
                    expressions__state_of_expression__in=form.cleaned_data[
                        "state_of_expression"
                    ]
                )
    context["form"] = formset
    context["objects_list"] = paged_object_list_context(request, d, paginate_by=10)
    print(d)
    return TemplateResponse(request, "describe/description_list.html", context)


def description_list(request):
    context = {}
    protocol = Protocol.objects.get(name="TP16/3")
    traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))
    formset = DescriptionFilterFormSet(initial=traits)
    queryset = Description.objects.all().prefetch_related("expressions")
    if request.POST:
        formset = DescriptionFilterFormSet(request.POST, initial=traits)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data["state_of_expression"]:
                    print(form.cleaned_data["state_of_expression"])
                    queryset = queryset.filter(
                        expressions__state_of_expression__in=form.cleaned_data[
                            "state_of_expression"
                        ]
                    )
    context.update(paged_object_list_context(request, queryset, paginate_by=10))
    context["formset"] = formset
    return TemplateResponse(request, "describe/description_list.html", context)


class DescriptionDetail(DetailView):
    model = Description
    context_object_name = "description"


class DescriptionDeleteView(DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description-list")


class ProtocolsList(ListView):
    model = Protocol
    template_name = "describe/protocols_list.html"
    context_object_name = "protocols"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


class ProtocolCreate(CreateView):
    model = Protocol
    fields = [
        "name",
        "specie",
        "url_ref",
    ]
    template_name = "describe/protocol_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context

    def get_success_url(self):
        return reverse("describe:protocol-update", args=(self.object.id,))


class ProtocolDelete(DeleteView):
    model = Protocol
    success_url = reverse_lazy("describe:protocols_list")


class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = "protocol"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


def protocol_update(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)
    if request.method == "POST":
        form = TraitFormSet(request.POST, instance=protocol)
        # form = TraitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("describe:protocol_detail", kwargs={"pk": protocol.pk})
            )
    else:
        form = TraitFormSet(instance=protocol)
    return render(
        request,
        "describe/protocol_manage.html",
        {"fs": form, "protocol": protocol, "nav_protocols": "active"},
    )


def description_update(request, pk):
    # Get the description object
    description = get_object_or_404(Description, pk=pk)
    # Collect all the existing expressions
    exist_expr = description.expressions.all()
    # This is the forms list
    forms = []
    if request.method == "POST":
        form_has_errors = False
        for expr_id, state_id in zip(
            request.POST.getlist("id"), request.POST.getlist("state_of_expression")
        ):
            if state_id:
                form = ExpressionForm({"id": expr_id, "state_of_expression": state_id})
                if form.is_valid():
                    # __import__('pdb').set_trace()
                    # expression, create = Expression.objects.get_or_create(**form.cleaned_data, description = description)
                    if exist_expr.filter(
                        pk=form.cleaned_data["id"]
                    ).exists() and not exist_expr.filter(
                        state_of_expression=form.cleaned_data["state_of_expression"]
                    ):
                        exist_expr.filter(pk=form.cleaned_data["id"]).update(
                            state_of_expression=form.cleaned_data["state_of_expression"]
                        )
                        print("Updated existing")
                    else:
                        if not exist_expr.filter(
                            state_of_expression=form.cleaned_data["state_of_expression"]
                        ):
                            new_expression = Expression()
                            new_expression.state_of_expression = form.cleaned_data[
                                "state_of_expression"
                            ]
                            new_expression.description = description
                            new_expression.save()
                            print("Created new")
                else:
                    form_has_errors = True
            else:
                if expr_id:
                    exist_expr.filter(pk=expr_id).delete()
                    print("Deleted")
        if not form_has_errors:
            return HttpResponseRedirect(
                reverse("describe:description_detail", args=(description.id,))
            )

    for trait in description.available_traits:
        if exist_expr.filter(state_of_expression__trait=trait).exists():
            e = exist_expr.get(state_of_expression__trait=trait)
            form = ExpressionForm(model_to_dict(e))
        else:
            form = ExpressionForm()
        form.fields["state_of_expression"].queryset = State.objects.filter(trait=trait)
        forms.append(form)
    formset = zip(forms, description.available_traits)
    return render(
        request, "describe/description_manage.html", context={"formset": formset}
    )


class ExpressionUpdate(UpdateView):
    model = Expression
    fields = "__all__"
    template_name = "describe/expression_update.html"


class DescriptionCreate(CreateView):
    model = Description
    fields = [
        "name",
        "protocol",
        "variety",
    ]
    template_name = "describe/description_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_descriptions"] = "active"
        return context

    def get_success_url(self):
        return reverse("describe:description-update", args=(self.object.id,))
