from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.catalog.serializers import CatalogCreateSerializer, CatalogListSerializer, CatalogDetailSerializer, \
    CatalogUpdateSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.catalog.models import Catalog


class CatalogCreateAPIView(CreateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogCreateSerializer
    permission_classes = [IsAdmin]


class CatalogListAPIView(ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class CatalogDetailAPIView(RetrieveAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogDetailSerializer
    lookup_field = 'guid'


class CatalogUpdateAPIView(UpdateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class CatalogDeleteAPIView(DestroyAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
