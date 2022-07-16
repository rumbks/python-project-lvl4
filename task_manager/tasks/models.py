from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User = get_user_model()


def stringify_user(self):
    return f"{self.first_name} {self.last_name}"


User.__str__ = stringify_user


class Task(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.CharField(max_length=1000, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="tasks_created_set",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tasks_assigned_set",
    )
    labels = models.ManyToManyField(Label, through="TaskToLabel", blank=True)
    date_created = models.DateTimeField(default=timezone.now)


class TaskToLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
