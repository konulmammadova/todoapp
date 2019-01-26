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
    deadline = models.DateField()
    slug = models.SlugField(unique=True)

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

