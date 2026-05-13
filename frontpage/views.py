from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import (
    login_not_required,  # ty:ignore[unresolved-import]
    login_required,
    user_passes_test,
)
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django_tables2 import RequestConfig

from breadcrumbs.utils import breadcrumbs_context, generate_breadcrumbs
from frontpage.forms import AdminUserUpdateForm, UserUpdateForm
from frontpage.tables import UserTable
from frontpage.templatetags.components import ListPageHeader
from frontpage.utils.htmx import htmx_response_trigger
from frontpage.views_decorators import htmx_render_block_from_params, is_htmx


def index(request):
    return TemplateResponse(request, "frontpage/index.html", {"nav_home": "active", "crumbs": None})


@login_not_required
def appearance_set(request):
    appearance = request.POST.get("appearance", "light")
    request.session["appearance"] = appearance
    return HttpResponse()


@user_passes_test(lambda user: user.is_staff)
@htmx_render_block_from_params()
def admin(request):
    queryset = User.objects.all()
    table_user = UserTable(queryset)
    RequestConfig(request).configure(table_user)
    header = ListPageHeader(page_title="Users", create_url=reverse("frontpage:user_create"), modal=True)
    crumbs = breadcrumbs_context([("Admin", "")])
    context = {"table_user": table_user, "page_obj": queryset, "header": header, **crumbs}
    return TemplateResponse(request, "frontpage/admin.html", context)


@user_passes_test(lambda user: user.is_staff)
def user_create(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return htmx_response_trigger(["usersUpdated", "closeModal"])
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "frontpage/admin_user_form.html", {"form": form})


@user_passes_test(lambda user: user.is_staff)
def admin_user_update(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            if is_htmx(request):
                return htmx_response_trigger(["usersUpdated", "closeModal"])
            return redirect("frontpage:admin")
    else:
        form = AdminUserUpdateForm(instance=user)
    return TemplateResponse(request, "frontpage/admin_user_form.html", {"form": form, "instance": user})


@user_passes_test(lambda user: user.is_staff)
def admin_password_update(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password set.")
            if is_htmx(request):
                return htmx_response_trigger(["closeModal"])
            return redirect("frontpage:admin")
    else:
        form = AdminPasswordChangeForm(user)
    context = {"user": user, "form": form}
    return TemplateResponse(request, "frontpage/admin_password_update_form.html", context)


@user_passes_test(lambda user: user.is_staff)
def user_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        user.delete()
        return htmx_response_trigger(["usersUpdated", "closeModal"])
    return TemplateResponse(request, "frontpage/user_confirm_delete.html", {"instance": user})


@login_required
def user_detail(request):
    return TemplateResponse(request, "frontpage/user_detail.html", generate_breadcrumbs(request, User, request.user))


@login_required
def user_update(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("frontpage:user_detail")
    else:
        form = UserUpdateForm(instance=user)
    crumbs = generate_breadcrumbs(request, User, request.user)
    context = {"form": form, **crumbs}
    return TemplateResponse(request, "frontpage/user_update.html", context)


@sensitive_post_parameters("old_password", "new_password1", "new_password2")
@csrf_protect
@login_required
def password_update(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated.")
            if is_htmx(request):
                return htmx_response_trigger(["closeModal"])
            return redirect("frontpage:user_detail")
    else:
        form = PasswordChangeForm(request.user)

    return TemplateResponse(request, "frontpage/password_update_form.html", {"form": form})
