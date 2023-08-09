from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.catalog.images.serializers import CatalogImageCreateSerializer, CatalogImageListSerializer, \
    CatalogImageDetailSerializer
from common.catalog.models import CatalogImage


class CatalogImageCreateAPIView(CreateAPIView):
    queryset = CatalogImage.objects.all()
    serializer_class = CatalogImageCreateSerializer
    permission_classes = [IsAdmin]


class CatalogImageListAPIView(ListAPIView):
    queryset = CatalogImage.objects.all()
    serializer_class = CatalogImageListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class CatalogImageDetailAPIView(RetrieveAPIView):
    queryset = CatalogImage.objects.all()
    serializer_class = CatalogImageDetailSerializer
    lookup_field = 'guid'


class CatalogImageUpdateAPIView(UpdateAPIView):
    queryset = CatalogImage.objects.all()
    serializer_class = CatalogImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class CatalogImageDeleteAPIView(DestroyAPIView):
    queryset = CatalogImage.objects.all()
    serializer_class = CatalogImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
