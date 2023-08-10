from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import Portfolio, PortfolioImage


class PortfolioCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'file3D', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'photos']


class PortfolioUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'file3D', 'description', 'description_uz',
                  'description_ru', 'description_en', 'photo', 'photos']


class PortfolioImagesDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = PortfolioImage
        fields = ['id', 'guid', 'photo_medium']


class PortfolioListSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'description', 'photo_medium']


class PortfolioDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, portfolio):
        portfolio_images = portfolio.portfolioImages.all()
        return PortfolioImagesDetailSerializer(portfolio_images, many=True).data

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'photos', 'file3D', 'description',
                  'description_uz', 'description_ru', 'description_en', 'photo_medium']
