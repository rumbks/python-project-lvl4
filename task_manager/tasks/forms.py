from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.logged_in_user = kwargs.pop("logged_in_user", None)
        super(TaskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels",
        ]
        localized_fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Assignee"),
            "labels": _("Labels"),
        }
        widgets = {
            "description": forms.Textarea(attrs={"cols": 40, "rows": 10}),
        }
