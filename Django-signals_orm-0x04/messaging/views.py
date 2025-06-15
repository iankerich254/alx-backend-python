from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message


@login_required
@cache_page(60)
def conversation_messages(request, user_id):
    """
    Display all top-level messages sent by the logged-in user to another user,
    including their threaded replies. Uses select_related and prefetch_related
    for query optimization.
    """
    messages = Message.objects.filter(
        sender=request.user,
        receiver_id=user_id,
        parent_message__isnull=True
    ).select_related('receiver').prefetch_related('replies')

    return render(request, 'messaging/conversation.html', {'messages': messages})


@login_required
def delete_user(request):
    """
    Delete the currently logged-in user and clean up all related data.
    """
    user = request.user
    logout(request)  # Ensure user is logged out before deletion
    user.delete()
    return redirect('login')


@login_required
def unread_messages(request):
    """
    Display unread messages for the current user using the custom manager.
    """
    unread = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread.html', {'unread_messages': unread})


@login_required
def threaded_message_view(request, message_id):
    """
    Display a specific message and all of its threaded replies.
    """
    root_message = get_object_or_404(Message, id=message_id)
    replies = Message.objects.filter(
        parent_message=root_message
    ).select_related('sender').prefetch_related('replies')

    return render(request, 'messaging/thread.html', {
        'root_message': root_message,
        'replies': replies,
    })

