from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Log

def log_action(action, instance):
    if action == 'create':
        username = instance.created_by.username if instance.created_by else None
    else:
        username = instance.updated_by.username if instance.updated_by else None

    Log.objects.create(
        action=action,
        table_name=instance.__class__.__name__,
        username=username
    )

@receiver(post_save)
def log_create_or_update(sender, instance, created, **kwargs):
    if sender._meta.app_label == 'home' and sender.__name__ not in ['Log']:
        action = 'create' if created else 'update'
        log_action(action, instance)

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.app_label == 'home' and sender.__name__ not in ['Log']:
        username = instance.deleted_by.username if instance.deleted_by else None
        Log.objects.create(
            action='delete',
            table_name=instance.__class__.__name__,
            username=username
        )