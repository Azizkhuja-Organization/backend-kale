from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.catalog.models import Catalog


class CatalogCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'file']


class CatalogUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'file']


class CatalogListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)
    description_ru = serializers.CharField()
    description_en = serializers.CharField()
    description_uz = serializers.CharField()

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'photo_small', 'file', 'description_ru', 'description_uz', 'description_en']


class CatalogDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo_medium', 'file']
