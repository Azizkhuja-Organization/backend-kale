from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.product.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True, write_only=True)

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo']


class CategoryListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo_small']


class CategoryDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo_medium']
