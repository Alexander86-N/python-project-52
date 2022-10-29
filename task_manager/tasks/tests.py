from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.users.models import ProjectUsers


class TestStatuses(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user_one = ProjectUsers.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="Vanek",
            password="badpass1"
        )
        cls.user_two = ProjectUsers.objects.create(
            first_name="Petr",
            last_name="Petrov",
            username="Petya",
            password="badpass2"
        )

        cls.first_status = Statuses.objects.create(name="Hello")
        cls.first_task = Tasks.objects.create(name="Дело",
                                              description="Пройти тест",
                                              author=cls.user_one,
                                              executor=cls.user_two,
                                              status=cls.first_status)

    def test_create_task(self):
        """Тест создания задачи."""

        self.client.force_login(self.user_two)
        response = self.client.post(
            reverse('create_task'), {
                "name": "Welcome",
                "description": "Новый тест пройден",
                "executor": 1,
                "status": 1
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tasks.objects.count(), 2)
        self.assertTrue(Tasks.objects.filter(name='Welcome').exists())
        self.assertRedirects(response, '/tasks/')

    def test_update_task(self):
        """Тест корректного изменения задачи."""

        self.client.force_login(self.user_one)
        url = reverse('update_task', args=(self.first_task.pk, ))
        response = self.client.post(url, {
            "name": "One more time",
            "description": "Новый тест не прошел, нужно изменить",
            "executor": 2,
            "status": 1
        }, follow=True)

        self.assertRedirects(response, '/tasks/')
        self.assertTrue(Tasks.objects.filter(name='One more time').exists())

    def test_dalete_task(self):
        """Тест удаления задачи."""

        self.client.force_login(self.user_one)
        url = reverse('delete_task', args=(self.first_task.id, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Tasks.objects.count(), 0)
        self.assertRedirects(response, '/tasks/')
