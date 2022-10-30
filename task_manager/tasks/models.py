from django.db import models
from task_manager.users.models import ProjectUsers
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    executor = models.ForeignKey(ProjectUsers,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 related_name='task_executor')
    author = models.ForeignKey(ProjectUsers,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='task_author')
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='task_status')
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Labels,
                                    blank=True,
                                    through='TaskLabels',
                                    through_fields=('task', 'label'),
                                    related_name='task_label')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class TaskLabels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)
