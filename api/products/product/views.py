from django.db.models import Q, Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.paginator import CustomPagination
from api.products.product.serializers import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer
from api.products.product.tasks import updateProducts
from common.order.models import Wishlist
from common.product.models import Product


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'unit', 'status', 'brand', 'manufacturer', 'cornerStatus', 'isTop']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user_id=self.request.user.id)
            queryset = queryset.annotate(isLiked=Exists(wishlist.products.all().filter(id__in=OuterRef('pk'))))

        hasLiked = self.request.query_params.get('hasLiked')
        if hasLiked:
            queryset = queryset.filter(isLiked=True)

        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass

        has3D = self.request.query_params.get('has3D')
        if has3D:
            queryset = queryset.filter(file3D__isnull=False)

        baseCategory = self.request.query_params.get('baseCategory')
        if baseCategory:
            queryset = queryset.filter(category__category=baseCategory)

        min = self.request.query_params.get('min')
        max = self.request.query_params.get('max')
        if min and max:
            queryset = queryset.filter(price__range=[min, max])
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'guid'


class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
