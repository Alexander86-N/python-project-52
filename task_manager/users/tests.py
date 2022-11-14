from django.test import TestCase
from django.urls import reverse
from .models import ProjectUsers


class HomePageTest(TestCase):
    """Тест домашней страницы."""

    def test_home_page_view(self):
        """Тест: корневой url преобразуется в страницу приветствия."""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class UsersModelTest(TestCase):

    fixtures = ['users.yaml']

    @classmethod
    def setUpTestData(cls):

        cls.first_user = ProjectUsers.objects.get(pk=1)

    def test_if_can_register_user(self):
        """Тест для проверки правильности регистрации пользователя."""

        response = self.client.post(reverse('sign_up'), {
            "first_name": "Petr",
            "last_name": "Petrov",
            "username": "Petrushka",
            "password1": "petr1111",
            "password2": "petr1111"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProjectUsers.objects.count(), 3)
        self.assertTrue(ProjectUsers.objects.filter(
            username='Petrushka'
        ).exists())
        self.assertRedirects(response, '/login/')

    def test_login_user(self):
        """Тест для проверки авторизации пользователя."""

        response = self.client.post(reverse('login'), {
            "username": "Vanek",
            "password": "fakepass1"
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_update_users(self):
        """Тест корректного изменения пользователя."""

        self.client.force_login(self.first_user)
        url = reverse('update_user', args=(self.first_user.id, ))
        response = self.client.post(url, {
            "first_name": "Ivanushka",
            "last_name": self.first_user.last_name,
            "username": self.first_user.username,
            "password1": "badpass2",
            "password2": "badpass2"
        }, follow=True)
        new_user = ProjectUsers.objects.get(username=self.first_user.username)

        self.assertRedirects(response, '/users/')
        self.assertTrue(new_user.check_password("badpass2"))

    def test_dalete_user(self):
        """Тест удаления пользователя."""

        self.client.force_login(self.first_user)
        url = reverse('delete_user', args=(self.first_user.id, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(ProjectUsers.objects.count(), 1)
        self.assertRedirects(response, '/users/')
