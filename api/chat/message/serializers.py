from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.chat.models import Message

User = get_user_model()


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'guid', 'sender', 'content']


class MessageSenderSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'photo_small']


class MessageListSerializer(serializers.ModelSerializer):
    sender = MessageSenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'guid', 'sender', 'content', 'timestamp']
