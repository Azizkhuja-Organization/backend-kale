from rest_framework import serializers

from common.social.models import Map


class MapCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'guid', 'title', 'phone', 'text', 'location', 'isMap']
