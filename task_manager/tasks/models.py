from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.CharField(max_length=1000, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="tasks_created_set",
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='tasks_assigned_set',
    )
    date_created = models.DateTimeField(default=timezone.now)
