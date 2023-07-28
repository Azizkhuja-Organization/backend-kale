from rest_framework import serializers

from api.cart.serializers import CartProductListSerializer
from common.order.models import Order, Checkout
from common.product.models import Product


class CheckoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'guid', 'user', 'products']


class CheckoutDetailSerializer(serializers.ModelSerializer):
    products = CartProductListSerializer(many=True)

    class Meta:
        model = Checkout
        fields = ['id', 'guid', 'user', 'products', 'amount']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'guid', 'checkout', 'product', 'isDelivery', 'orderedTime', 'deliveredTime']


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'guid', 'checkout', 'product', 'isDelivery', 'orderedTime', 'deliveredTime', 'status']


class OrderProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'price', 'material', 'unit', 'brand', 'size', 'manufacturer',
                  'photo_small']


class OrderDetailSerializer(serializers.ModelSerializer):
    product = OrderProductDetailSerializer(many=False)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'checkout', 'product', 'isDelivery', 'orderedTime', 'deliveredTime', 'status']
