from django.forms import ModelForm
from task_manager.labels.models import Labels
from django.utils.translation import gettext


class LabelsForm(ModelForm):

    class Meta:
        model = Labels
        fields = ["name"]
        labels = {"name": gettext("Имя")}
