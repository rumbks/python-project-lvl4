from django.urls import path
from task_manager.users.views import ListUsers

app_name = 'users'

urlpatterns = [
    path('', ListUsers.as_view(), name='list'),
]
