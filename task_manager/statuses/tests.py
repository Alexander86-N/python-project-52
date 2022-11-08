from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Statuses
from task_manager.users.models import ProjectUsers
from task_manager.tasks.models import Tasks


class TestStatuses(TestCase):

    fixtures = ['users.yaml',
                'statuses.yaml',
                'tasks.yaml',
                'labels.yaml']

    @classmethod
    def setUpTestData(cls):

        cls.user = ProjectUsers.objects.get(pk=1)
        cls.task = Tasks.objects.get(pk=12)
        cls.status_one = Statuses.objects.get(pk=1)
        cls.status_two = Statuses.objects.get(pk=3)
        cls.status_three = Statuses.objects.get(pk=4)

    def test_create_status(self):
        """Тест создания статуса."""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_status'),
            {"name": "Welcome"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.count(), 4)
        self.assertTrue(Statuses.objects.filter(name='Welcome').exists())
        self.assertRedirects(response, '/statuses/')

    def test_update_status(self):
        """Тест корректного изменения статуса."""

        self.client.force_login(self.user)
        url = reverse('update_status', args=(self.status_one.id, ))
        response = self.client.post(url, {"name": "Good bye"}, follow=True)

        self.assertRedirects(response, '/statuses/')
        self.assertTrue(Statuses.objects.filter(name='Good bye').exists())

    def test_dalete_status(self):
        """Тест удаления статуса."""

        self.client.force_login(self.user)
        url = reverse('delete_status', args=(self.status_three.pk, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Statuses.objects.count(), 2)
        self.assertRedirects(response, '/statuses/')

    def test_list_of_all_statuses(self):
        """Тест получения списка всех статусов."""

        self.client.force_login(self.user)
        response = self.client.get(reverse('list_of_all_statuses'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context['statuses_list']),
            [self.status_one, self.status_two, self.status_three]
        )

    def test_an_unsecured_user_tries_to_view_the_statuses(self):
        """Тест незалогиненный пользователь пытается посмотреть статусы."""

        response = self.client.get(reverse('list_of_all_statuses'))

        self.assertRedirects(response, '/login/')

    def test_delete_the_status_that_is_being_used(self):
        """Тест попытка удалить статус который используется."""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_status', args=(self.status_two.pk, )),
            follow=True
        )

        self.assertRedirects(response, '/statuses/')
        self.assertEqual(Statuses.objects.count(), 3)
        self.assertTrue(Statuses.objects.filter(name='Срочно!').exists())
