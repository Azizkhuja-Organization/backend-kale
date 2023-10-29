from django.db import transaction
from rest_framework import serializers

from common.address.models import Address
from common.order.models import Order, OrderProduct, CartProduct
from common.payment.payme.models import PaymentType
from common.product.models import Product
from common.users.models import User
from config.settings.base import env
from kale.contrib.payment_utils import create_initialization_payme, create_initialization_click


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
        discount = data.get('discount', 0.0)

        if data['orderPrice'] < discount:
            error_message = "Discount field is greater than available orderPrice"
            raise serializers.ValidationError({"discount": [error_message]})

        if product.quantity < quantity:
            error_message = "Requested quantity is greater than available quantity for the product."
            raise serializers.ValidationError({"quantity": [error_message]})

        return data

class OrderCreateSerializerV2(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = OrderCreateOrderProductSerializer(many=True, write_only=True)
    billing_url = serializers.CharField(allow_null=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'installation', 'comment', 'paymentType', 'billing_url']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order_products = []
        totalAmount = 0
        for product_data in products_data:
            order_product = OrderProduct.objects.create(**product_data)
            totalAmount += product_data['orderPrice'] if product_data['discount'] == 0 else product_data['discount']
            order_products.append(order_product)

        order_instance = Order.objects.create(**validated_data)
        order_instance.products.set(order_products)
        if validated_data['paymentType'] == PaymentType.PAYME:
            billing_url = create_initialization_payme(totalAmount, order_instance.id)
        elif validated_data['paymentType'] == PaymentType.CLICK:
            billing_url = create_initialization_click(totalAmount, order_instance.id)
        else:
            billing_url = None
        order_instance.billing_url = billing_url
        return order_instance
