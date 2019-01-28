from django.contrib import admin

# Register your models here.
from todolist.models import Task, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'task', 'content', 'created_at')


class TaskCommentInline(admin.TabularInline):
    model = Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'user')
    inlines = [
        TaskCommentInline,
    ]
