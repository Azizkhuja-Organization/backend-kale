from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.order.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer, \
    CheckoutCreateSerializer, CheckoutDetailSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient, IsAdmin
from common.order.models import Order, Checkout


class CheckoutCreateAPIView(CreateAPIView):
    queryset = Checkout.objects.select_related('user').prefetch_related('products', 'products__product')
    serializer_class = CheckoutCreateSerializer
    permission_classes = [IsClient]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        checkout, created = Checkout.objects.get_or_create(user=request.user)
        checkout.products.set(serializer.data.get('products'))
        checkout.save()
        return Response(CheckoutCreateSerializer(checkout).data, status=status.HTTP_201_CREATED)


class CheckoutDetailAPIView(RetrieveAPIView, DestroyAPIView):
    queryset = Checkout.objects.select_related('user').prefetch_related('products').all()
    serializer_class = CheckoutDetailSerializer
    permission_classes = [IsClient]
    lookup_field = 'guid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = request.query_params.get('productId')
        if product:
            instance.products.remove(product)
        return Response(status=status.HTTP_200_OK)


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsAdmin]


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.select_related('checkout', 'product').all()
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['checkout', 'product', 'status']
    permission_classes = [IsClient | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start and end:
            queryset = queryset.filter(created_at__range=[start, end])
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(quantity=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'


class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'
