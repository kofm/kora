import logging

from django.contrib.admin.sites import login_not_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django_tables2 import RequestConfig

from frontpage.forms import UserUpdateForm
from frontpage.tables import UserTable
from frontpage.utils.htmx import htmx_response_trigger
from frontpage.utils.logging import get_client_ip
from frontpage.views_decorators import htmx_render_block_from_params

logger = logging.getLogger("kora.failed_login")


def index(request):
    return TemplateResponse(request, "frontpage/index.html", {"nav_home": "active", "crumbs": None})


@login_not_required
def appearance_set(request):
    appearance = request.POST.get("appearance", "light")
    request.session["appearance"] = appearance
    return HttpResponse()


@user_passes_test(lambda user: user.is_superuser)
@htmx_render_block_from_params()
def admin(request):
    queryset = User.objects.prefetch_related("groups").all()
    table_user = UserTable(queryset)
    RequestConfig(request).configure(table_user)
    context = {"table_user": table_user, "page_obj": queryset}
    return TemplateResponse(request, "frontpage/admin.html", context)


@user_passes_test(lambda user: user.is_superuser)
def user_create(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return htmx_response_trigger(["usersUpdated", "closeModal"])
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "frontpage/user_create.html", {"form": form})


@user_passes_test(lambda user: user.is_superuser)
def user_update(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return htmx_response_trigger(["usersUpdated", "closeModal"])
    else:
        form = UserUpdateForm(instance=user)
    return TemplateResponse(request, "frontpage/user_create.html", {"form": form, "instance": user})


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        user.delete()
        return htmx_response_trigger(["usersUpdated", "closeModal"])
    return TemplateResponse(request, "frontpage/user_confirm_delete.html", {"instance": user})


class KoraLoginView(LoginView):
    def form_invalid(self, form):
        client_ip = get_client_ip(self.request)
        logger.warning("FAILED LOGIN for user '%s' from %s", form.cleaned_data["username"], client_ip)
        return super().form_invalid(form)
