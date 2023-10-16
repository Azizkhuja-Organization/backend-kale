from rest_framework import serializers

from api.products.product.serializers import ProductDetailSerializer
from api.users.serializers import UserListSerializer
from common.order.models import Cart, CartProduct
from common.product.models import Product
from config.settings.base import env


# CART

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'guid', 'user']


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'guid', 'user', 'total_price']


class CartDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'guid', 'user', 'total_price']


# CART PRODUCTS

class CartProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'guid', 'cart', 'product', 'quantity', 'orderPrice']


class CartProductSerializer(serializers.ModelSerializer):
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'title', 'code', 'price', 'oldPrice', 'photo_small', 'cornerStatus', 'discount', 'quantity']


class CartProductListSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    isLiked = serializers.BooleanField(default=False)
    isCompared = serializers.BooleanField(default=False)

    class Meta:
        model = CartProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'isLiked', 'isCompared']


class CartProductDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice']
