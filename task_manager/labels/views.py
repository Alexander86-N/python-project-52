from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.contrib import messages
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Labels
from .forms import LabelsForm


class ListOfAllLabels(LoginRequiredMixin, ListView):

    model = Labels
    template_name = 'labels/list_of_all_labels.html'
    context_object_name = 'labels_list'


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin,
                  CreateView, FormView):

    model = Labels
    template_name = 'labels/create_label.html'
    form_class = LabelsForm
    success_url = reverse_lazy('list_of_labels')
    success_message = gettext('Метка успешно создана')


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin,
                  UpdateView, FormView):

    model = Labels
    template_name = 'labels/update_label.html'
    form_class = LabelsForm
    success_url = reverse_lazy('list_of_labels')
    success_message = gettext('Метка успешно изменена')


class DeleteLabel(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Labels
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('list_of_labels')

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, gettext("Невозможно удалить метку,\
                потому что она используется"))
        else:
            messages.success(self.request,
                             gettext('Метка успешно удалена'))
        return redirect(self.success_url)
