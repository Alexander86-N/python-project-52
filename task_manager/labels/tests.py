from django.test import TestCase
from django.urls import reverse, reverse_lazy
from task_manager.users.models import ProjectUsers
from task_manager.labels.models import Labels
from task_manager.tasks.models import Tasks


class TestLabels(TestCase):

    fixtures = ['users.yaml',
                'tasks.yaml',
                'statuses.yaml',
                'labels.yaml']

    @classmethod
    def setUpTestData(cls):

        cls.user = ProjectUsers.objects.get(pk=1)
        cls.first_task = Tasks.objects.get(pk=12)
        cls.first_label = Labels.objects.get(pk=1)
        cls.second_label = Labels.objects.get(pk=8)
        cls.third_label = Labels.objects.get(pk=3)

    def test_create_label(self):
        """Тест корректного создания метки."""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_label'),
            {"name": "pig"},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.count(), 4)
        self.assertTrue(Labels.objects.filter(name='pig').exists())
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
        url = reverse('delete_label', args=(self.second_label.pk, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Labels.objects.count(), 2)
        self.assertRedirects(response, '/labels/')

    def test_list_of_all_labels(self):
        """Тест получения списка всех меток."""

        self.client.force_login(self.user)
        response = self.client.get(reverse('list_of_labels'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context['labels_list']),
            [self.first_label, self.third_label, self.second_label]
        )

    def test_an_unsecured_user_tries_to_view_the_label(self):
        """Тест незалогиненный пользователь пытается посмотреть метку."""

        response = self.client.get(reverse('list_of_labels'))

        self.assertRedirects(response, '/login/')

    def test_delete_the_label_whose_task_is_marked(self):
        """Тест попытка удалить метку действующей задачи."""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('delete_label', args=(self.third_label.pk, )),
            follow=True
        )

        self.assertRedirects(response, '/labels/')
        self.assertEqual(Labels.objects.count(), 3)
        self.assertTrue(Labels.objects.filter(name='bug').exists())
