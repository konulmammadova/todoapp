from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView, RedirectView, CreateView, DetailView

from todolist.forms import RegisterForm, LoginForm, AddTaskForm
from todolist.models import Task
from todolist.tasks import post_signup_welcome_mail


class IndexView(TemplateView):
    template_name ='todoapp/index.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'todoapp/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        new_user.set_password(password)
        new_user.save()

        # Send the user a welcome mail
        post_signup_welcome_mail(new_user.pk)

        messages.success(self.request, 'Uğurla qeydiyyatdan keçdiniz! Zəhmət olmasa daxil olun.')
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'todoapp/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    permanent = False
    pattern_name = 'index'
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


# @login_required(login_url='login')
class DashboardView(ListView):
    model = Task
    template_name = 'todoapp/dashboard.html'
    context_object_name = 'tasks'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(DashboardView, self).dispatch(*args, **kwargs)

# @login_required(login_url='login')
class AddTaskView(CreateView):
    model = Task
    form_class = AddTaskForm
    success_url = reverse_lazy('dashboard')
    template_name = 'todoapp/add-task.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super(AddTaskView, self).form_valid(form)

# class EditTaskView():
#     pass
#
# class DeleteTaskView():
#     pass


# @login_required(login_url='login')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'todoapp/task-detail.html'
    slug_field = 'slug'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['created_by'] = self.request.user.get_full_name
        return context
