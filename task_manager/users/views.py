from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView


class ListUsers(ListView):
    model = get_user_model()
    template_name = 'users_list.html'



