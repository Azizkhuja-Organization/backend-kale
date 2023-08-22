from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.catalog.models import Catalog, CatalogImage
from config.settings.base import env


class CatalogCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'photos']


class CatalogUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'photos']


class CatalogListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, portfolio):
        if portfolio.photo:
            if not "http" in portfolio.photo.url:
                return env('BASE_URL') + portfolio.photo.url
            return portfolio.photo.url
        return None

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'photo_small', 'file']


class CatalogImagesDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, portfolio):
        if portfolio.photo:
            if not "http" in portfolio.photo.url:
                return env('BASE_URL') + portfolio.photo.url
            return portfolio.photo.url
        return None

    class Meta:
        model = CatalogImage
        fields = ['id', 'guid', 'photo_medium', 'file']


class CatalogDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    def get_file(self, portfolio):
        if portfolio.photo:
            if not "http" in portfolio.photo.url:
                return env('BASE_URL') + portfolio.photo.url
            return portfolio.photo.url
        return None

    def get_photos(self, catalog):
        catalog_images = catalog.catalogImages.all()
        return CatalogImagesDetailSerializer(catalog_images, many=True).data

    class Meta:
        model = Catalog
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo_medium', 'photos', 'file']
