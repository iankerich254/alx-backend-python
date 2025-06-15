from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Message, Notification, MessageHistory
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_msg = Message.objects.get(pk=instance.pk)
        if old_msg.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old_msg.content)
            instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
