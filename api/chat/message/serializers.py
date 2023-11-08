from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.chat.models import Message
from config.settings.base import env

User = get_user_model()


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'guid', 'sender', 'content']


class MessageSenderSerializer(serializers.ModelSerializer):
    #photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'photo_small']


class MessageListSerializer(serializers.ModelSerializer):
    sender = MessageSenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'guid', 'sender', 'content', 'timestamp']
