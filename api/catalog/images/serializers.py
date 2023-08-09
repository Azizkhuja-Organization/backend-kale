from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.catalog.models import CatalogImage


class CatalogImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = CatalogImage
        fields = ['id', 'guid', 'catalog', 'photo']


class CatalogImageListSerializer(serializers.ModelSerializer):
    catalog = serializers.CharField(source='catalog.title')
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = CatalogImage
        fields = ['id', 'guid', 'catalog', 'photo_small']


class CatalogImageDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = CatalogImage
        fields = ['id', 'guid', 'photo_medium']
