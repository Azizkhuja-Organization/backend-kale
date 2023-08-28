from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.banner.models import Banner, SmallBanner, PointerNumber


class BannerCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Banner
        fields = ['id', 'guid', 'photo', 'url']


class BannerListSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'guid', 'photo_medium', 'url']


class SmallBannerCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = SmallBanner
        fields = ['id', 'guid', 'photo', 'url']


class SmallBannerListSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = SmallBanner
        fields = ['id', 'guid', 'photo_medium', 'url']


class PointerNumberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointerNumber
        fields = ['id', 'guid', 'client', 'product', 'project', 'delivered']
