from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import ProjectUsers
from task_manager.labels.models import Labels


class TestLabels(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = ProjectUsers.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="Vanek",
            password="badpass1"
        )
        cls.first_label = Labels.objects.create(name="Срочно")

    def test_create_label(self):
        """Тест корректного создания метки."""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_label'),
            {"name": "bug"},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.count(), 2)
        self.assertTrue(Labels.objects.filter(name='bug').exists())
        self.assertRedirects(response, '/labels/')

    def test_update_label(self):
        """Тест корректного изменения метки."""

        self.client.force_login(self.user)
        url = reverse('update_label', args=(self.first_label.id, ))
        response = self.client.post(url, {"name": "question"}, follow=True)

        self.assertRedirects(response, '/labels/')
        self.assertTrue(Labels.objects.filter(name='question').exists())

    def test_dalete_label(self):
        """Тест удаления метки."""

        self.client.force_login(self.user)
        url = reverse('delete_label', args=(self.first_label.pk, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Labels.objects.count(), 0)
        self.assertRedirects(response, '/labels/')
