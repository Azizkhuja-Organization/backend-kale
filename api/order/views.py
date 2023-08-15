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
from common.users.models import User


class CheckoutCreateAPIView(CreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutCreateSerializer
    permission_classes = [IsClient]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data.get('products'):
            return Response({"error": "Product is not chosen"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        if self.request.user.role == User.UserRole.CLIENT:
            queryset = queryset.filter(checkout__user=self.request.user)
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start and end:
            queryset = queryset.filter(
                created_at__gte=start,
                created_at__lte=end
            )
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(product__title__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.select_related('checkout', 'product').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'


class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
