from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.news.models import News
from config.settings.base import env


class NewsCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'videoURL', 'status', 'isActual']


class NewsUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'videoURL', 'status', 'isActual']


class NewsListSerializer(serializers.ModelSerializer):
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'photo_small', 'videoURL', 'viewCount', 'created_at', 'status', 'isActual',
                  'description']


class NewsDetailSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz', 'status',
                  'description_ru', 'description_en', 'photo_medium', 'videoURL', 'videoURL', 'viewCount', 'created_at',
                  'isActual']
