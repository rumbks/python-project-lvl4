from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from task_manager.users.forms import UserForm


class ListUsers(ListView):
    model = get_user_model()
    template_name = 'users_list.html'


class CreateUser(CreateView):
    model = get_user_model()
    template_name = 'user_create.html'
    form_class = UserForm
    success_url = reverse_lazy('main')


class UpdateUser(UpdateView):
    model = get_user_model()
    template_name = 'user_update.html'
    form_class = UserForm
    success_url = reverse_lazy('users:list')


class DeleteUser(DeleteView):
    model = get_user_model()
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users:list')
