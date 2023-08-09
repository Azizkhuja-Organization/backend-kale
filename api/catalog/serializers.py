from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.catalog.models import Catalog, CatalogImage


class CatalogCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'photos']


class CatalogListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'photo_small']


class CatalogImagesDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = CatalogImage
        fields = ['id', 'guid', 'photo_medium']


class CatalogDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, catalog):
        catalog_images = catalog.catalogImages.all()
        return CatalogImagesDetailSerializer(catalog_images, many=True).data

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo_medium', 'photos']
