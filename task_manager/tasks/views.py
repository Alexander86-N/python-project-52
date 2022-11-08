from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.contrib import messages
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.utils import WithoutAccessMixin
from .models import Tasks
from .forms import TasksForm
from .filters import TasksFilter


class ListOfAllTasks(LoginRequiredMixin, WithoutAccessMixin, FilterView):

    model = Tasks
    template_name = 'tasks/list_of_all_tasks.html'
    context_object_name = 'tasks_list'
    filterset_class = TasksFilter


class CreateTask(LoginRequiredMixin, SuccessMessageMixin,
                 CreateView, FormView):

    model = Tasks
    template_name = 'tasks/create_task.html'
    form_class = TasksForm
    success_url = reverse_lazy('list_of_tasks')
    success_message = gettext('Задача успешно создана')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin,
                 UpdateView, FormView):

    model = Tasks
    template_name = 'tasks/update_task.html'
    form_class = TasksForm
    success_url = reverse_lazy('list_of_tasks')
    success_message = gettext('Задача успешно изменена')


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Tasks
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('list_of_tasks')
    success_message = gettext('Задача успешно удалена')

    def form_valid(self, form):
        if self.get_object().author == self.request.user:
            return super().form_valid(form)
        else:
            messages.error(self.request,
                           gettext("Задачу может удалить только её автор"))
            return redirect(self.success_url)


class ViewTask(LoginRequiredMixin, SuccessMessageMixin, DetailView):

    model = Tasks
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
