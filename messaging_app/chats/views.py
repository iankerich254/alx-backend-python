from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.
# 3a. ConversationViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, destroy for Conversation.
    Only authenticated users can create/list their own conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production

    def get_queryset(self):
        # Optionally limit to conversations that include the requesting user
        user = self.request.user
        if user and user.is_authenticated:
            return Conversation.objects.filter(participants=user).order_by('-created_at')
        return Conversation.objects.none()

    def perform_create(self, serializer):
        # When creating, ensure the requesting user is included
        participants = serializer.validated_data.get('participants', [])
        if self.request.user.is_authenticated and self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save()

    @action(detail=True, methods=['post'], url_path='add-participant')
    def add_participant(self, request, pk=None):
        """
        Custom action to add a participant to an existing conversation.
        Payload: { "user_id": <int> }
        """
        conversation = self.get_object()
        target_user = get_object_or_404(User, pk=request.data.get('user_id'))
        conversation.participants.add(target_user)
        return Response({'status': 'participant added'}, status=status.HTTP_200_OK)

# 3b. MessageViewSet
class MessageViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, destroy for Message.
    """
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated

    def perform_create(self, serializer):
        """
        Override to set sender based on the requesting user.
        Expect the request body to include "conversation": <conversation_id>, "content": <text>.
        """
        user = self.request.user
        if not user.is_authenticated:
            # In production, raise PermissionDenied or return an error
            raise PermissionDenied("Authentication required to send a message.")

        conversation_id = self.request.data.get('conversation')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Optionally: ensure the user is a participant
        if user not in conversation.participants.all():
            return Response(
                {'detail': 'User is not part of this conversation.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=user, conversation=conversation)
