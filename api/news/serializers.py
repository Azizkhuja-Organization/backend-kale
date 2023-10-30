from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.news.models import News


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
    photo_small = serializers.ImageField(read_only=True)
    short_description_uz = serializers.SerializerMethodField()
    short_description_ru = serializers.SerializerMethodField()
    short_description_en = serializers.SerializerMethodField()

    def get_short_description_uz(self, obj):
        if obj.description_uz:
            return obj.description[:100]  # Return the first 100 characters of the description
        else:
            return None

    def get_short_description_ru(self, obj):
        if obj.description_ru:
            return obj.description[:100]  # Return the first 100 characters of the description
        else:
            return None

    def get_short_description_en(self, obj):
        if obj.description_en:
            return obj.description[:100]  # Return the first 100 characters of the description
        else:
            return None

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'photo_small', 'videoURL', 'viewCount', 'created_at', 'status', 'isActual',
                  'short_description_uz', 'short_description_ru', 'short_description_en']


class NewsDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'description_uz', 'status',
                  'description_ru', 'description_en', 'photo_medium', 'videoURL', 'videoURL', 'viewCount', 'created_at',
                  'isActual']
