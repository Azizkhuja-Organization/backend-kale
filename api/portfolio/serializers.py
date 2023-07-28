from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import Portfolio


class PortfolioCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'file3D', 'description', 'photo']


class PortfolioDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, portfolio):
        return [image.url for image in portfolio.portfolioImages.all() if image]

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'images', 'file3D', 'description', 'photo_medium']
