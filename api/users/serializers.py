from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from config.settings.base import env

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo']


class UserUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo']


class UserListSerializer(serializers.ModelSerializer):
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo_small']


class UserDetailSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo_medium']
