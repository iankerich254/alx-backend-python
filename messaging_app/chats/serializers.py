from rest_framework import serializers
from django.conf import settings
from .models import Conversation, Message, User

# 2a. UserSerializer (Expose only necessary fields)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # or settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'display_name', 'email']

# 2b. MessageSerializer: shows sender details but not full nested conversation
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']

# 2c. ConversationSerializer: include participants (list of user IDs) and nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    # For nested output, you can include messages as a read-only nested field
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages']

    def create(self, validated_data):
        """
        Override create() to handle m2m participants.
        """
        participants_data = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants_data)
        return conversation
