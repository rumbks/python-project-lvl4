from django.urls import path
from task_manager.users.views import ListUsers, CreateUser, UpdateUser, DeleteUser

app_name = 'users'

urlpatterns = [
    path('', ListUsers.as_view(), name='list'),
    path('create/', CreateUser.as_view(), name='create'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete'),
]
