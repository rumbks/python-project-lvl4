from django.utils.translation import gettext_lazy as _
from django import forms
import django_filters

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        label=_("Label"),
        queryset=Label.objects.all(),
    )
    is_mine = django_filters.BooleanFilter(
        label=_('My tasks only'),
        method='filter_is_mine',
        widget=forms.CheckboxInput(),
    )

    def filter_is_mine(self, queryset, name, is_selected):
        author = self.request.user
        if is_selected:
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'assignee']
