from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import LoginRequiredMixin, ProtectedObjectMixin
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class ListLabels(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'


class CreateLabel(SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:list')
    success_message = _("Label was successfully created")


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:list')
    success_message = _("Label was successfully updated")


class DeleteLabel(
    LoginRequiredMixin, ProtectedObjectMixin, SuccessMessageMixin, DeleteView
):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = _("Label was successfully deleted")
    protected_failure_message = _("You can't delete in-use label")
    failure_url = reverse_lazy('labels:list')
