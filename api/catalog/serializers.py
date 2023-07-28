from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.catalog.models import Catalog


class CatalogCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'description', 'photo']


class CatalogListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'photo_small']


class CatalogDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'description', 'photo_medium']
