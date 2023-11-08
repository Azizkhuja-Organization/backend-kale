from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import PortfolioImage
from config.settings.base import env


class PortfolioImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'portfolio', 'photo']


class PortfolioImageListSerializer(serializers.ModelSerializer):
    portfolio = serializers.CharField(source='product.title')
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'portfolio', 'photo_small']


class PortfolioImageDetailSerializer(serializers.ModelSerializer):
    # photo_medium = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'photo_medium']
