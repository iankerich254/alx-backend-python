from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Conversation, Message

# Register your models here.
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    # If you added custom fields (display_name), include them
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('display_name',)}),
    )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'timestamp')
    list_filter = ('conversation', 'sender', 'timestamp')
