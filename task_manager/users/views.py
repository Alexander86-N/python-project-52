from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.urls import reverse_lazy
from task_manager.utils import WithoutAccessMixin, WithAccessMixin
from .models import ProjectUsers
from .forms import SignInForm, SignUpForm


class ListOfUsers(ListView):
    model = ProjectUsers
    template_name = 'users/users_list.html'
    context_object_name = "users_list"


class RegistrationUser(SuccessMessageMixin, CreateView, FormView):

    model = ProjectUsers
    template_name = 'users/registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = gettext("Пользователь успешно зарегистрирован")


class UserLogin(SuccessMessageMixin, LoginView, FormView):

    model = ProjectUsers
    template_name = 'users/login.html'
    form_class = SignInForm
    next_page = reverse_lazy('home')
    success_message = gettext("Вы залогинены")


class UserLogout(SuccessMessageMixin, LogoutView):

    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS,
                             gettext("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(LoginRequiredMixin, WithoutAccessMixin, WithAccessMixin,
                 SuccessMessageMixin, UpdateView, FormView):

    model = ProjectUsers
    template_name = 'users/update_user.html'
    form_class = SignUpForm
    success_url = reverse_lazy('list_of_users')
    success_message = gettext("Пользователь успешно изменён")
    error_output = "У вас нет прав для изменения другого пользователя."
    error_url = reverse_lazy('list_of_users')


class DeleteUser(LoginRequiredMixin, WithoutAccessMixin, WithAccessMixin,
                 SuccessMessageMixin, DeleteView, FormView):

    model = ProjectUsers
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('list_of_users')
    success_message = gettext("Пользователь успешно удалён")
    error_output = "У вас нет прав для изменения другого пользователя."
    error_url = reverse_lazy('list_of_users')
