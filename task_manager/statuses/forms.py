from django.forms import ModelForm
from django.utils.translation import gettext
from task_manager.statuses.models import Statuses


class StatusesForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ['name']
        labels = {'name': gettext('Имя')}
