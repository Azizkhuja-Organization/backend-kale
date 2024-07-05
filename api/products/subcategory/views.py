from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.products.subcategory.serializers import SubCategoryCreateSerializer, SubCategoryDetailSerializer, \
    SubCategoryListSerializer
from common.product.models import SubCategory
from config.settings.base import CACHE_TTL


class SubCategoryCreateAPIView(CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    permission_classes = [IsAdmin]


class SubCategoryListAPIView(ListAPIView):
    serializer_class = SubCategoryListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    pagination_class = CustomPagination

    def get_queryset(self):
        return SubCategory.objects.select_related('category').order_by('id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            queryset = queryset.exclude(guid=guid)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryDetailAPIView(RetrieveAPIView):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategoryDetailSerializer
    lookup_field = 'guid'


class SubCategoryUpdateAPIView(UpdateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class SubCategoryDeleteAPIView(DestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
