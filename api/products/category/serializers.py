from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from common.product.models import Category
from config.settings.base import env


class CategoryCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True, write_only=True)

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'photo']


class CategorySubCategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'guid', 'title']


class CategoryListSerializer(serializers.ModelSerializer):
    # photo_small = serializers.ImageField(read_only=True)
    subcategories = serializers.SerializerMethodField()
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    def get_subcategories(self, category):
        subcategories = category.categorySubCategories
        if subcategories:
            return CategorySubCategoriesListSerializer(subcategories, many=True).data
        return []

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo_small', 'subcategories']


class CategoryDetailSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'title_ru', 'title_uz', 'title_en', 'photo_medium']
