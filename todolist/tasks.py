# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task
def post_signup_welcome_mail(user_pk=None):
    print('In post_signup_welcome_maul User PK: {}'.format(user_pk))
    user = User.objects.filter(pk=user_pk).first()
    if user:
        print('Welcome user {}'.format(user.username))
    else:
        print('User not found')
