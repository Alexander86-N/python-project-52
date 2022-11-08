from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy


class WithoutAccessMixin(AccessMixin):

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("Вы не авторизованы! Пожалуйста, выполните вход.")
        )
        return redirect(reverse_lazy('login'))


class WithAccessMixin(AccessMixin):
    error_output = ''
    error_url = ''

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(self.request, gettext(self.error_output))
            return redirect(self.error_url)
        return super().dispatch(request, *args, **kwargs)


class DeletingAnElementMixin(AccessMixin):
    error_message = ''
    success_massage = ''
    redirect_url = ''

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, gettext(self.error_message))
        else:
            messages.success(self.request,
                             gettext(self.success_message))
        return redirect(self.redirect_url)
