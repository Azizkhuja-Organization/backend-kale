from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.partner.models import Partner


class PartnerCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Partner
        fields = ['id', 'guid', 'title', 'description', 'photo']


class PartnerListSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Partner
        fields = ['id', 'guid', 'title', 'photo_small']


class PartnerDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Partner
        fields = ['id', 'guid', 'title', 'description', 'photo_medium']
