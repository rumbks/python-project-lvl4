from django.urls import path
from task_manager.tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.ListTasks.as_view(), name='list'),
    path('create/', views.CreateTask.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='delete'),
    path('<int:pk>/', views.TaskDetails.as_view(), name='details'),
]
