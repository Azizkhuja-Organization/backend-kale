from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.news.models import News


class NewsCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'videoURL', 'status']


class NewsUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'videoURL', 'status']


class NewsListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'photo_small', 'videoURL', 'viewCount', 'created_at', 'status']


class NewsDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz', 'status',
                  'description_ru', 'description_en', 'photo_medium', 'videoURL', 'videoURL', 'viewCount', 'created_at']
