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

    @classmethod
    def setUpTestData(cls):

        ProjectUsers.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            username="Vanek",
            password="badpass1"
        )

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
        self.assertEqual(ProjectUsers.objects.count(), 2)
        self.assertTrue(ProjectUsers.objects.filter(
            username='Petrushka'
        ).exists())
        self.assertRedirects(response, '/login/')

    def test_login_user(self):
        """Тест для проверки авторизации пользователя."""

        response = self.client.post(reverse('login'), {
            "username": "Vanek",
            "password": "badpass1"
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_update_users(self):
        """Тест корректного изменения пользователя."""

        user = ProjectUsers.objects.get(pk=1)
        self.client.force_login(user)
        url = reverse('update_user', args=(user.id, ))
        response = self.client.post(url, {
            "first_name": "Ivanushka",
            "last_name": user.last_name,
            "username": user.username,
            "password1": "badpass2",
            "password2": "badpass2"
        }, follow=True)
        new_user = ProjectUsers.objects.get(username=user.username)

        self.assertRedirects(response, '/users/')
        self.assertTrue(new_user.check_password("badpass2"))

    def test_dalete_user(self):
        """Тест удаления пользователя."""

        user = ProjectUsers.objects.get(pk=1)
        self.client.force_login(user)
        url = reverse('delete_user', args=(user.id, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(ProjectUsers.objects.count(), 0)
        self.assertRedirects(response, '/users/')
