from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext
from django.urls import reverse_lazy
from task_manager.utils import WithoutAccessMixin, DeletingAnElementMixin
from .models import Labels
from .forms import LabelsForm


class ListOfAllLabels(LoginRequiredMixin, WithoutAccessMixin, ListView):

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


class DeleteLabel(LoginRequiredMixin, DeletingAnElementMixin,
                  SuccessMessageMixin, DeleteView):

    model = Labels
    template_name = 'labels/delete_label.html'
    redirect_url = reverse_lazy('list_of_labels')
    error_message = "Невозможно удалить метку, потому что она используется"
    success_message = "Метка успешно удалена"
