from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Notification
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

# Create your views here.
@login_required
@cache_page(60)
def conversation_messages(request, user_id):
    """
    Display all messages between the current user and another user
    (threaded format), with 60-second view cache.
    """
    messages = Message.objects.filter(
        receiver_id=user_id,
        parent_message__isnull=True
    ).select_related('sender').prefetch_related('replies')

    return render(request, 'messaging/conversation.html', {'messages': messages})


@login_required
def delete_user(request):
    """
    Delete the currently logged-in user and clean up all related data.
    """
    user = request.user
    logout(request)  # Log out the user before deletion
    user.delete()
    return redirect('login')


@login_required
def unread_messages(request):
    """
    Display unread messages for the current user using the custom manager.
    """
    unread = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread.html', {'unread_messages': unread})


@login_required
def threaded_message_view(request, message_id):
    """
    Display a message and its threaded replies using ORM recursion.
    """
    root_message = get_object_or_404(Message, id=message_id)
    thread = Message.objects.filter(parent_message=root_message).select_related('sender').prefetch_related('replies')

    return render(request, 'messaging/thread.html', {
        'root_message': root_message,
        'replies': thread,
    })
