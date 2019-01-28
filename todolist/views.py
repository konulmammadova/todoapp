from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView, RedirectView, CreateView, DetailView

from todolist.forms import RegisterForm, LoginForm, AddTaskForm, CommentForm
from todolist.models import Task
from todolist.tasks import send_mail_alert_deadline


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

        messages.success(self.request, 'Uğurla qeydiyyatdan keçdiniz! Zəhmət olmasa daxil olun.')
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'todoapp/login.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

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


class DashboardView(ListView):
    model = Task
    template_name = 'todoapp/dashboard.html'
    # slug_field = 'slug'
    context_object_name = 'tasks'


    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class AddTaskView(CreateView):
    '''
        View for adding new tasks
        Also
    '''
    model = Task
    form_class = AddTaskForm
    success_url = reverse_lazy('dashboard')
    template_name = 'todoapp/add-task.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()

        alert_time = task.deadline - timedelta(minutes=1)
        send_mail_alert_deadline.apply_async((task.id,), eta=alert_time)

        return super(AddTaskView, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(AddTaskView, self).dispatch(request, *args, **kwargs)

# class EditTaskView():
#     pass
#
# class DeleteTaskView():
#     pass


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todoapp/task-detail.html'
    # slug_field = 'slug'
    # context_object_name = 'task'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            form = CommentForm()
            context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            # ! assign the object to self
            self.object = self.get_object()
            comment.task = self.object
            comment.save()
            context = super(TaskDetailView, self).get_context_data(**kwargs)
            context['form'] = CommentForm()
            return self.render_to_response(context=context)
        else:
            # ! assign the object to self
            self.object = self.get_object()
            context = super(TaskDetailView, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context=context)

