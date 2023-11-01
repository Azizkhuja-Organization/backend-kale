from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.portfolio.models import Portfolio, PortfolioImage
from config.settings.base import env


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
    file = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    def get_photos(self, portfolio):
        portfolio_images = portfolio.portfolioImages.all()
        return [{
            "id": portfolioImage.id,
            "guid": portfolioImage.guid,
            "title": portfolioImage.title,
            "photo_medium": env('BASE_URL') + portfolioImage.photo_medium.url
        } for portfolioImage in portfolio_images if not "http" in portfolioImage.photo_medium.url]

    def get_file(self, portfolio):
        if portfolio.photo:
            if not "http" in portfolio.photo.url:
                return env('BASE_URL') + portfolio.photo.url
            return portfolio.photo.url
        return None

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'description', 'photo_medium', 'file', 'photos', 'logo']


class PortfolioDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    def get_photos(self, portfolio):
        portfolio_images = portfolio.portfolioImages.all()
        return [{
            "id": portfolioImage.id,
            "title": portfolioImage.title,
            "guid": portfolioImage.guid,
            "photo_medium": env('BASE_URL') + portfolioImage.photo_medium.url
        } for portfolioImage in portfolio_images if not "http" in portfolioImage.photo_medium.url]

    def get_file(self, portfolio):
        if portfolio.photo:
            if not "http" in portfolio.photo.url:
                return env('BASE_URL') + portfolio.photo.url
            return portfolio.photo.url
        return None

    class Meta:
        model = Portfolio
        fields = ['id', 'guid', 'title', 'title_uz', 'title_ru', 'title_en', 'photos', 'file3D', 'description',
                  'description_uz', 'description_ru', 'description_en', 'photo_medium', 'file', 'logo']
