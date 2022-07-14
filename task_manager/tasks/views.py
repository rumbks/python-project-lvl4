from django.contrib.auth.views import get_user_model
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import LoginRequiredMixin, OwnershipRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class ListTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['logged_in_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = form.logged_in_user
        self.object.save()
        form._save_m2m()
        return super().form_valid(form)

    model = Task
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')
    success_message = _("Task was successfully created")


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    model = Task
    template_name = 'tasks/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')
    success_message = _("Task was successfully updated")


class DeleteTask(
    LoginRequiredMixin, OwnershipRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    model_user_id_field_name = 'author_id'
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _("Task was successfully deleted")
    failure_url = reverse_lazy('tasks:list')
    failure_message = _("Task can be deleted by it's author only")


class TaskDetails(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/details.html'
