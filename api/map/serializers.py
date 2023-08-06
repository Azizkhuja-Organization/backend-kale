from rest_framework import serializers

from common.social.models import Map


class MapCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'phone', 'text', 'text_uz', 'text_ru',
                  'text_en', 'location', 'isMap']


class MapListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'guid', 'title', 'phone', 'text', 'location', 'isMap']
