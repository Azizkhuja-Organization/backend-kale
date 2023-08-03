from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import Portfolio, PortfolioImage


class PortfolioCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'file3D', 'description', 'photo']


class PortfolioImagesDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = PortfolioImage
        fields = ['photo_medium']

class PortfolioDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, portfolio):
        portfolio_images = portfolio.portfolioImages.all()
        return PortfolioImagesDetailSerializer(portfolio_images, many=True).data

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'photos', 'file3D', 'description', 'photo_medium']
