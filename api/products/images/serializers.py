from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from common.product.models import ProductImage


class ProductImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'product', 'photo']


class ProductImageListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title')
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'product', 'photo_small']


class ProductImageDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['photo_medium']
