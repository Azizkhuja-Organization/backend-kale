from django.db.models import Q, Prefetch
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.products.category.serializers import CategoryCreateSerializer, CategoryListSerializer, CategoryDetailSerializer
from common.product.models import Category, SubCategory


# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie

# from config.settings.base import CACHE_TTL


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdmin]


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoryListSerializer

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
            queryset = queryset.filter(
                Q(title__icontains=q)
            )
        queryset = queryset.prefetch_related(
            Prefetch(
                lookup='categorySubCategory',
                queryset=SubCategory.objects.all(),
                to_attr="categorySubCategories"
            )
        )
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'guid'


class CategoryUpdateAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
