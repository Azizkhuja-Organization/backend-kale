from django.db.models import Q
from api.permissions import IsAdmin
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.map.serializers import MapCreateSerializer
from api.paginator import CustomPagination
from common.social.models import Map


class MapCreateAPIView(CreateAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    permission_classes = [IsAdmin]


class MapListAPIView(ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(phone__icontains=q))
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