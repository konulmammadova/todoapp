from django.contrib.auth.models import User
from django import forms

from todolist.models import Task, Comment


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password': forms.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Task Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'deadline': forms.DateTimeInput(
                                attrs={'placeholder': 'deadline like: 2019-03-25 14:30:59', 'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}),
        }
