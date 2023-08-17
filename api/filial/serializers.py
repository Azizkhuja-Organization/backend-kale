from rest_framework import serializers

from common.social.models import Filial


class FilialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ['id', 'guid', 'social', 'title', 'title_uz', 'title_ru', 'title_en', 'description', 'location',
                  'phone']


class FilialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ['id', 'guid', 'title', 'location', 'phone']
