from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

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
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo_small']


class UserDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo_medium']
