from task_manager.users.models import ProjectUsers
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from .models import Tasks
from django import forms
from django.utils.translation import gettext
from django_filters.filterset import FilterSet
from django_filters.filters import ModelChoiceFilter, BooleanFilter


class TasksFilter(FilterSet):

    status = ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=gettext("Статус")
    )
    executor = ModelChoiceFilter(
        queryset=ProjectUsers.objects.all(),
        label=gettext("Исполнитель")
    )
    labels = ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=gettext("Метка")
    )

    my_tasks = BooleanFilter(
        widget=forms.CheckboxInput(),
        method='only_your_own_tasks',
        label=gettext('Только свои задачи')
    )

    def only_your_own_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user)

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels']
