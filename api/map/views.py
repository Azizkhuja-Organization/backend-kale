from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.map.serializers import MapCreateSerializer, MapListSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.social.models import Map
from config.settings.base import CACHE_TTL


class MapCreateAPIView(CreateAPIView):
    queryset = Map.objects.all()
    serializer_class = MapCreateSerializer
    permission_classes = [IsAdmin]


class MapListAPIView(ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapListSerializer
    pagination_class = CustomPagination

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
