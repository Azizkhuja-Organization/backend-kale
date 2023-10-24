from django.db import transaction
from rest_framework import serializers

from common.address.models import Address
from common.order.models import Order, OrderProduct, CartProduct
from common.product.models import Product
from common.users.models import User
from config.settings.base import env


class OrderProductProductDetailSerializer(serializers.ModelSerializer):
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()



    def get_photo_small(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'unit', 'brand', 'size', 'photo_small']


class OrderProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'discount']


class OrderProductListSerializer(serializers.ModelSerializer):
    product = OrderProductProductDetailSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'discount']


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
        fields = ['id', 'guid', 'user', 'products', 'address', 'installation', 'comment', 'paymentType', 'totalAmount',
                  'deliveredTime', 'paymentStatus', 'paymentType', 'status']


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


class OrderCreateOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'discount']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if product.quantity < quantity:
            raise serializers.ValidationError("Requested quantity is greater than available quantity for the product.")

        return data

class OrderCreateSerializerV2(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = OrderCreateOrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'installation', 'comment', 'paymentType']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order_instance = super().create(validated_data)

        for product_data in products_data:
            product_data['order'] = order_instance.id
            OrderProduct.objects.create(order=order_instance, **product_data)

        return order_instance
