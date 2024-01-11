from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Chat, ChatMessage

class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'users', 'updated_at_formatted',)


class ChatMessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    sent_to = UserSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = ('id', 'body', 'created_by', 'sent_to', 'created_at_formatted',)


class ChatDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'users', 'messages', 'updated_at_formatted',)