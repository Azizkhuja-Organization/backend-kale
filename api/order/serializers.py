from rest_framework import serializers

from common.order.models import Order, OrderProduct
from common.product.models import Product
from common.users.models import User


class OrderProductProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'unit', 'brand', 'size', 'photo_small']


class OrderProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice']


class OrderProductListSerializer(serializers.ModelSerializer):
    product = OrderProductProductDetailSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice']


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    # products = serializers.PrimaryKeyRelatedField(
    #     queryset=CartProduct.objects.all(), many=True)
    installation = serializers.BooleanField()
    paymentType = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'installation', 'comment', 'paymentType']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'installation', 'comment', 'paymentType']


class OrderListSerializer(serializers.ModelSerializer):
    products = OrderProductListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'code', 'products', 'totalAmount', 'orderedTime', 'deliveredTime', 'comment',
                  'paymentStatus', 'paymentType', 'status']


class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'totalAmount', 'orderedTime', 'deliveredTime',
                  'installation', 'comment', 'installation', 'paymentStatus', 'paymentType', 'status']
