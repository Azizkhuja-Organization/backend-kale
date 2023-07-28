from rest_framework import serializers

from common.order.models import Wishlist
from common.product.models import Product


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'guid', 'user', 'products']


class WishlistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'guid', 'user', 'products']


class WishlistProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'price', 'material', 'size', 'photo_small', 'cornerStatus']


class WishlistDetailSerializer(serializers.ModelSerializer):
    products = WishlistProductDetailSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'guid', 'products']
