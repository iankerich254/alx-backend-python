from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1a. Custom User (optional; if no extra fields are needed, skip this and use auth.User)
class User(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.username

# 1b. Conversation Model: tracks participants
class Conversation(models.Model):
    # Many-to-many to users
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    # Optionally: a title or last_updated timestamp, created_at
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Show participant usernames joined by commas
        names = [user.username for user in self.participants.all()]
        return "Conversation between: " + ", ".join(names)

# 1c. Message Model: each message belongs to a single conversation
class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} @ {self.timestamp:%Y-%m-%d %H:%M}: {self.content[:20]}…"
