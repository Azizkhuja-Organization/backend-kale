from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.map.serializers import MapCreateSerializer, MapListSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.social.models import Map


class MapCreateAPIView(CreateAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    permission_classes = [IsAdmin]


class MapListAPIView(ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class MapDetailAPIView(RetrieveAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    lookup_field = 'guid'


class MapUpdateAPIView(UpdateAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class MapDestroyAPIView(DestroyAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
