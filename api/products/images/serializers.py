from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.product.models import ProductImage
from config.settings.base import env


class ProductImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'product', 'photo']


class ProductImageListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title')
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'product', 'photo_small']


class ProductImageDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'photo_medium']
