from django.urls import path
from task_manager.statuses import views

app_name = 'statuses'

urlpatterns = [
    path('', views.ListStatuses.as_view(), name='list'),
    path('create/', views.CreateStatus.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateStatus.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteStatus.as_view(), name='delete'),
]
