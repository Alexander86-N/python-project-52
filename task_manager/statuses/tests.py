from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Statuses
from task_manager.users.models import ProjectUsers


class TestStatuses(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = ProjectUsers.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="Vanek",
            password="badpass1"
        )
        cls.first_status = Statuses.objects.create(name="Hello")

    def test_create_status(self):

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_status'),
            {"name": "Welcome"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.count(), 2)
        self.assertTrue(Statuses.objects.filter(name='Welcome').exists())
        self.assertRedirects(response, '/statuses/')

    def test_update_status(self):
        """Тест корректного изменения статуса."""

        self.client.force_login(self.user)
        url = reverse('update_status', args=(self.first_status.id, ))
        response = self.client.post(url, {"name": "Good bye"}, follow=True)

        self.assertRedirects(response, '/statuses/')
        self.assertTrue(Statuses.objects.filter(name='Good bye').exists())

    def test_dalete_status(self):
        """Тест удаления статуса."""

        self.client.force_login(self.user)
        url = reverse('delete_status', args=(self.first_status.pk, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Statuses.objects.count(), 0)
        self.assertRedirects(response, '/statuses/')
