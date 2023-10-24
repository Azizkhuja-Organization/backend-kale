from django.db.models import Q
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.order.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer, \
    OrderUpdateSerializer, OrderCreateSerializerV2, OrderCreateOrderProductSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient, IsAdmin
from common.order.models import Order, CartProduct, OrderProduct, OrderStatus, PaymentTypes, PaymentStatus
from common.users.models import User


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsAdmin]

    def create(self, request, *args, **kwargs):
        products = request.data.pop('products')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cartProducts = CartProduct.objects.filter(id__in=products)
        if not cartProducts or not products:
            return Response({"products": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        orderProducts = []
        totalAmount = 0
        for p in cartProducts:
            orderProducts.append(OrderProduct(product=p.product, quantity=p.quantity, orderPrice=p.orderPrice, discount=p.product.discount))
            totalAmount += p.orderPrice
        OrderProduct.objects.bulk_create(orderProducts)
        order = serializer.save()
        if order.paymentType == PaymentTypes.CASH:
            order.status = OrderStatus.PENDING
        order.products.set(orderProducts)
        order.totalAmount = totalAmount
        order.save()
        cartProducts.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related('products', 'products__product').select_related('user', 'address').all()
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'installation', 'paymentStatus', 'paymentType', 'status']
    permission_classes = [IsClient | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.UserRole.CLIENT:
            queryset = queryset.filter(Q(user=self.request.user) & (
                    Q(paymentStatus=PaymentStatus.REJECTED) |
                    Q(paymentStatus=PaymentStatus.REFUNDED) |
                    Q(paymentStatus=PaymentStatus.CONFIRMED) |
                    Q(paymentType=PaymentTypes.CASH)))
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start and end:
            queryset = queryset.filter(
                created_at__gte=start,
                created_at__lte=end
            )
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related('products', 'products__product').select_related('user', 'address').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'


class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class OrderCreateAPIViewV2(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializerV2
    permission_classes = [IsClient]

