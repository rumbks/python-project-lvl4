from django.db import models
from django.utils import timezone


class Label(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
