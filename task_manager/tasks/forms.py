from django.forms import ModelForm
from django.utils.translation import gettext
from task_manager.tasks.models import Tasks


class TasksForm(ModelForm):

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'executor', 'status', 'labels']
        labels = {"name": gettext("Имя"),
                  "description": gettext("Описание"),
                  "executor": gettext("Исполнитель"),
                  "status": gettext("Статус"),
                  "labels": gettext("Метки")
                  }
