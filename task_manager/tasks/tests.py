from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.users.models import ProjectUsers
from django_filters.filterset import FilterSet
from django_filters.filters import ModelChoiceFilter


class TestTasks(TestCase):

    fixtures = ['users.yaml',
                'statuses.yaml',
                'tasks.yaml',
                'labels.yaml']

    @classmethod
    def setUpTestData(cls):

        cls.first_user = ProjectUsers.objects.get(pk=1)
        cls.second_user = ProjectUsers.objects.get(pk=2)
        cls.status = Statuses.objects.get(pk=3)
        cls.first_task = Tasks.objects.get(pk=12)
        cls.second_task = Tasks.objects.get(pk=13)

    def test_create_task(self):
        """Тест создания задачи."""

        self.client.force_login(self.second_user)
        response = self.client.post(
            reverse('create_task'), {
                "name": "Welcome",
                "description": "Новый тест пройден",
                "executor": 1,
                "status": 1
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tasks.objects.count(), 3)
        self.assertTrue(Tasks.objects.filter(name='Welcome').exists())
        self.assertRedirects(response, '/tasks/')

    def test_update_task(self):
        """Тест корректного изменения задачи."""

        self.client.force_login(self.first_user)
        url = reverse('update_task', args=(self.first_task.pk, ))
        response = self.client.post(url, {
            "name": "One more time",
            "description": "Новый тест не прошел, нужно изменить",
            "executor": 2,
            "status": 3
        }, follow=True)

        self.assertRedirects(response, '/tasks/')
        self.assertTrue(Tasks.objects.filter(name='One more time').exists())

    def test_dalete_task(self):
        """Тест удаления задачи."""

        self.client.force_login(self.first_user)
        url = reverse('delete_task', args=(self.first_task.id, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(Tasks.objects.count(), 1)
        self.assertRedirects(response, '/tasks/')

    def test_filter_found_for_status(self):
        """Тест проверки фильтра по Статусу."""

        instance = Tasks._meta.get_field("status")
        result = FilterSet.filter_for_field(instance, "status")

        self.assertIsInstance(result, ModelChoiceFilter)
        self.assertEqual(result.field_name, "status")

    def test_filter_found_for_executor(self):
        """Тест проверки фильтра по Исполнитель."""

        instance = Tasks._meta.get_field("executor")
        result = FilterSet.filter_for_field(instance, "executor")

        self.assertIsInstance(result, ModelChoiceFilter)
        self.assertEqual(result.field_name, "executor")

    def test_filter_found_for_labels(self):
        """Тест проверки фильтра по Метка."""

        instance = Tasks._meta.get_field("labels")
        result = FilterSet.filter_for_field(instance, "labels")

        self.assertEqual(result.field_name, "labels")

    def test_list_of_all_tasks(self):
        """Тест получения списка всех задач."""

        self.client.force_login(self.first_user)
        response = self.client.get(reverse('list_of_tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context['tasks_list']),
            [self.first_task, self.second_task]
        )

    def test_delete_a_task_if_not_the_author(self):
        """Тест удаление чужой задачи."""

        self.client.force_login(self.second_user)
        response = self.client.post(
            reverse('delete_task', args=(self.first_task.pk, )),
            follow=True
        )

        self.assertRedirects(response, '/tasks/')
        self.assertTrue(Tasks.objects.filter(name='Test').exists())

    def test_an_unsecured_user_tries_to_view_the_tasks(self):
        """Тест незалогиненный пользователь пытается посмотреть задачи."""

        response = self.client.get(reverse('list_of_tasks'))

        self.assertRedirects(response, '/login/')
