from django.db.models.signals import pre_save
from django.dispatch import receiver
from todolist.models import Task
from todolist.tools import slugify


@receiver(pre_save, sender=Task, dispatch_uid='signal_create_task_slug')
def signal_create_product_slug(*args, **kwargs):
    instance = kwargs.get('instance')
    if not instance.slug or instance.name_cache != instance.name:
        instance.name_cache = instance.name
        instance.slug = slugify(instance.name)
        instance.save()
