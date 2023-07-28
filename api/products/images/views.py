from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.paginator import CustomPagination
from api.products.images.serializers import ProductImageCreateSerializer, ProductImageListSerializer, \
    ProductImageDetailSerializer
from common.product.models import ProductImage


class ProductImageCreateAPIView(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAuthenticated]


class ProductImageListAPIView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class ProductImageDetailAPIView(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class ProductImageUpdateAPIView(UpdateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class ProductImageDeleteAPIView(DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
