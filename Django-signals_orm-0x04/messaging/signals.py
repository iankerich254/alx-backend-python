from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification  # Import the Message and Notification models

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
