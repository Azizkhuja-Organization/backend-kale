from django.db.models import Q
from api.permissions import IsAdmin
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.catalog.serializers import CatalogCreateSerializer, CatalogListSerializer, CatalogDetailSerializer
from api.paginator import CustomPagination
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
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass
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
    serializer_class = CatalogCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class CatalogDeleteAPIView(DestroyAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
