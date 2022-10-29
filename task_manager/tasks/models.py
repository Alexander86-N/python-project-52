from django.db import models
from task_manager.users.models import ProjectUsers
from task_manager.statuses.models import Statuses


class Tasks(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    executor = models.ForeignKey(ProjectUsers,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 related_name='executors')
    author = models.ForeignKey(ProjectUsers,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='authors')
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='statuses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
