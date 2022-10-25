from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext
# from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Statuses
from .forms import StatusesForm
# from task_manager.users.views import WithoutAccessMixin


class ListOfAllStatuses(LoginRequiredMixin, ListView):

    model = Statuses
    template_name = 'statuses/list_of_all_statuses.html'
    context_object_name = 'statuses_list'


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin,
                   CreateView, FormView):

    model = Statuses
    template_name = 'statuses/create_status.html'
    form_class = StatusesForm
    success_url = reverse_lazy('list_of_all_statuses')
    success_message = gettext('Статус успешно создан')


class UpdateStatus(SuccessMessageMixin,
                   UpdateView, FormView):

    model = Statuses
    template_name = 'statuses/update_status.html'
    form_class = StatusesForm
    success_url = reverse_lazy('list_of_all_statuses')
    success_message = gettext('Статус успешно изменён')


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('list_of_all_statuses')
    success_message = gettext('Статус успешно удалён')
#    message_error = 'Невозможно удалить статус, потому что он используется'
#
#    def dispatch(self, request, *args, **kwargs):
#        if self.request.user != self.get_object():
#            messages.error(self.request, gettext(message_error))
#            return redirect(reverse_lazy('list_of_all_statuses'))
#        return super().dispatch(request, *args, **kwargs)
