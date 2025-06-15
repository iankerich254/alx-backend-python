from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification, MessageHistory

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
