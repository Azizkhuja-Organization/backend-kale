from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.paginator import CustomPagination
from api.wishlist.serializers import WishlistCreateSerializer, WishlistListSerializer, WishlistDetailSerializer
from common.order.models import Wishlist
from common.product.models import Product


class WishlistAddSubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return Response(status=status.HTTP_200_OK)


class WishlistProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user_id=request.user)
        return Response(WishlistDetailSerializer(wishlist).data, status=status.HTTP_200_OK)


class WishlistCreateAPIView(CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistCreateSerializer
    permission_classes = [IsAuthenticated]


class WishlistListAPIView(ListAPIView):
    queryset = Wishlist.objects.select_related('user').prefetch_related('products').all()
    serializer_class = WishlistListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class WishlistDetailAPIView(RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class WishlistUpdateAPIView(UpdateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
