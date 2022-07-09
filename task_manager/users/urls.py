from django.urls import path
from task_manager.users.views import ListUsers, CreateUser

app_name = 'users'

urlpatterns = [
    path('', ListUsers.as_view(), name='list'),
    path('create/', CreateUser.as_view(), name='create'),
]
