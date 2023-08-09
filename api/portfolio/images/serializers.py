from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import PortfolioImage


class PortfolioImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'portfolio', 'photo']


class PortfolioImageListSerializer(serializers.ModelSerializer):
    portfolio = serializers.CharField(source='product.title')
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'portfolio', 'photo_small']


class PortfolioImageDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'photo_medium']
