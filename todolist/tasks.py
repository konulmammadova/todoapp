# Create your tasks here

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

from todoapp.settings import EMAIL_HOST_USER
from todolist.models import Task


@shared_task
def send_mail_alert_deadline(task_id):
    task = Task.objects.filter(id=task_id)
    if task:
        send_mail(subject='Alert',
                  message=f'TASK: {task.name} \n DESCRIPTION: {task.description} \n DEADLINE: {task.deadline}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[task.user.email],
                  fail_silently=False)
