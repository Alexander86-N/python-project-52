from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import ProjectUsers
from .forms import SignInForm, SignUpForm


WITHOUT_ACCESS = "Вы не авторизованы! Пожалуйста, выполните вход."
WITH_ACCESS = "У вас нет прав для изменения другого пользователя."


class WithoutAccessMixin(AccessMixin):

    def handle_no_permission(self):
        messages.error(self.request, gettext(WITHOUT_ACCESS))
        return redirect(reverse_lazy('login'))

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(self.request, gettext(WITH_ACCESS))
            return redirect(reverse_lazy('list_of_users'))
        return super().dispatch(request, *args, **kwargs)


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


class UpdateUser(LoginRequiredMixin, WithoutAccessMixin, SuccessMessageMixin,
                 UpdateView, FormView):

    model = ProjectUsers
    template_name = 'users/update_user.html'
    form_class = SignUpForm
    success_url = reverse_lazy('list_of_users')
    success_message = gettext("Пользователь успешно изменён")


class DeleteUser(LoginRequiredMixin, WithoutAccessMixin, SuccessMessageMixin,
                 DeleteView, FormView):

    model = ProjectUsers
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('list_of_users')
    success_message = gettext("Пользователь успешно удалён")
