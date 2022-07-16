from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import LoginRequiredMixin, ProtectedObjectMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class ListStatuses(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/list.html"


class CreateStatus(SuccessMessageMixin, CreateView):
    model = Status
    template_name = "statuses/create.html"
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status was successfully created")


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = "statuses/update.html"
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status was successfully updated")


class DeleteStatus(
    LoginRequiredMixin, ProtectedObjectMixin, SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status was successfully deleted")
    protected_failure_message = _("You can't delete in-use status")
    failure_url = reverse_lazy("statuses:list")
