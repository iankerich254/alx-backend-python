from rest_framework import serializers
from django.conf import settings
from .models import Conversation, Message, User

# 2a. UserSerializer (Expose only necessary fields)
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User  # or settings.AUTH_USER_MODEL
        fields = ['user_id', 'username', 'full_name', 'email', 'phone_number']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# 2b. MessageSerializer: shows sender details but not full nested conversation
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'message_preview']
        read_only_fields = ['message_id', 'sender', 'sent_at', 'message_preview']

    def get_message_preview(self, obj):
        return obj.message_body[:30] + '...' if len(obj.message_body) > 30 else obj.message_body

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

# 2c. ConversationSerializer: include participants (list of user IDs) and nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'messages']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants_data)
        return conversation
