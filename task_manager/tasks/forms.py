from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.logged_in_user = kwargs.pop('logged_in_user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'assignee',
        ]
        localized_fields = [
            'name',
            'description',
            'status',
            'assignee',
        ]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'assignee': _('Assignee'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }