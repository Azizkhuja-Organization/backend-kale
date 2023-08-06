from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.products.images.serializers import ProductImageCreateSerializer, ProductImageListSerializer, \
    ProductImageDetailSerializer
from common.product.models import ProductImage


class ProductImageCreateAPIView(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdmin]


class ProductImageListAPIView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class ProductImageDetailAPIView(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageDetailSerializer
    lookup_field = 'guid'


class ProductImageUpdateAPIView(UpdateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class ProductImageDeleteAPIView(DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
