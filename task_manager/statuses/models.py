from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(unique=True, max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
