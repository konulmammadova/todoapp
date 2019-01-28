import random
import string


from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
from django.urls import reverse

from todolist.tools import slugify


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()
    slug = models.SlugField(unique=True)
    # allowed_users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.name_cache = self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'slug': self.slug})

    """ 
    Permissions are 2 types:
    1. Model Level Permission - if you want to give permmissions on all Task models
    2. Object level Permission - if you want to give permissions on per-task basis
    
    This is model level permission
    """
    # class Meta:
    #     permissions = (
    #         ("view_task", "Can see the task"),
    #         ("write_comment", "Can write comment to the task"),
    #     )


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, models.CASCADE)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content}'

    # class Meta:
    #     permissions = (
    #         ('view_task', 'View task'),
    #         ('view_comment', 'View Comment'),
    #         ('add_comment', 'Add Comment'),
    #     )