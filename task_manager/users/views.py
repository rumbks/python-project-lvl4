from django.contrib.auth.views import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import (
    LoginRequiredMixin,
    OwnershipRequiredMixin,
    ProtectedObjectMixin,
)
from task_manager.users.forms import UserForm


class ListUsers(ListView):
    model = get_user_model()
    template_name = "users/list.html"


class CreateUser(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = "users/create.html"
    form_class = UserForm
    success_url = reverse_lazy("login")
    success_message = _("User was successfully registered")


class UpdateUser(
    LoginRequiredMixin, OwnershipRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = get_user_model()
    template_name = "users/update.html"
    form_class = UserForm
    success_url = reverse_lazy("users:list")
    success_message = _("User was successfully updated")
    failure_message = _("You have no permissions to update other user")
    failure_url = reverse_lazy("users:list")
    model_user_id_field_name = "id"


class DeleteUser(
    LoginRequiredMixin,
    OwnershipRequiredMixin,
    ProtectedObjectMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = get_user_model()
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User was successfully deleted")
    failure_message = _("You have no permissions to update other user")
    protected_failure_message = _("You can't delete in-use user")
    failure_url = reverse_lazy("users:list")
    model_user_id_field_name = "id"
