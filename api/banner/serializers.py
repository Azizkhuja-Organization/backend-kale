from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.banner.models import Banner, SmallBanner, PointerNumber, HeaderDiscount
from config.settings.base import env


class BannerCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()
    photo2 = Base64ImageField()
    photo3 = Base64ImageField()

    class Meta:
        model = Banner
        fields = ['id', 'guid', 'photo', 'photo2', 'photo3', 'url']


class BannerListSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    # photo_medium2 = serializers.ImageField(read_only=True)
    # photo_medium3 = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()
    photo_medium2 = serializers.SerializerMethodField()
    photo_medium3 = serializers.SerializerMethodField()

    def get_photo_medium3(self, banner):
        if banner.photo3:
            return env('BASE_URL') + banner.photo_medium3.url
        return None

    def get_photo_medium2(self, banner):
        if banner.photo2:
            return env('BASE_URL') + banner.photo_medium2.url
        return None

    def get_photo_medium(self, banner):
        if banner.photo:
            return env('BASE_URL') + banner.photo_medium.url
        return None

    class Meta:
        model = Banner
        fields = ['id', 'guid', 'photo_medium', 'photo_medium2', 'photo_medium3', 'url']


class SmallBannerCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()
    photo2 = Base64ImageField()
    photo3 = Base64ImageField()

    class Meta:
        model = SmallBanner
        fields = ['id', 'guid', 'photo', 'photo2', 'photo3', 'url']


class SmallBannerListSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    # photo_medium2 = serializers.ImageField(read_only=True)
    # photo_medium3 = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()
    photo_medium2 = serializers.SerializerMethodField()
    photo_medium3 = serializers.SerializerMethodField()

    def get_photo_medium3(self, banner):
        if banner.photo3:
            return env('BASE_URL') + banner.photo_medium3.url
        return None

    def get_photo_medium2(self, banner):
        if banner.photo2:
            return env('BASE_URL') + banner.photo_medium2.url
        return None

    def get_photo_medium(self, banner):
        if banner.photo:
            return env('BASE_URL') + banner.photo_medium.url
        return None

    class Meta:
        model = SmallBanner
        fields = ['id', 'guid', 'photo_medium', 'photo_medium2', 'photo_medium3', 'url']


class PointerNumberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointerNumber
        fields = ['id', 'guid', 'client', 'product', 'project', 'delivered']


class HeaderDiscountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderDiscount
        fields = ['id', 'guid', 'text', 'text_ru', 'text_en', 'text_uz', 'enabled']
