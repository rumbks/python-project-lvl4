from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from task_manager.users.forms import CreateUserForm


class ListUsers(ListView):
    model = get_user_model()
    template_name = 'users_list.html'


class CreateUser(CreateView):
    model = get_user_model()
    template_name = 'user_create.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('main')

