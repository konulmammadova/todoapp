from django.contrib import admin

# Register your models here.
from todolist.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'user')
