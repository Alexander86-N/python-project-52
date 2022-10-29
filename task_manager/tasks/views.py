# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Tasks
from .forms import TasksForm


class ListOfAllTasks(LoginRequiredMixin, ListView):

    model = Tasks
    template_name = 'tasks/list_of_all_tasks.html'
    context_object_name = 'tasks_list'


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
