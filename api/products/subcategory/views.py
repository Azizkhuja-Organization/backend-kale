from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.paginator import CustomPagination
from api.products.subcategory.serializers import SubCategoryCreateSerializer
from common.product.models import SubCategory


class SubCategoryCreateAPIView(CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    # permission_classes = [IsAuthenticated]


class SubCategoryListAPIView(ListAPIView):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategoryCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            queryset = queryset.exclude(guid=guid)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class SubCategoryDetailAPIView(RetrieveAPIView):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategoryCreateSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class SubCategoryUpdateAPIView(UpdateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class SubCategoryDeleteAPIView(DestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
