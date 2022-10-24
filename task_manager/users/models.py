from django.contrib.auth.models import AbstractUser


class ProjectUsers(AbstractUser):

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'ProjectUser'
        verbose_name_plural = 'ProjectUsers'
