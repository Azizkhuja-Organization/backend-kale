from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.news.serializers import NewsCreateSerializer, NewsListSerializer, NewsDetailSerializer
from api.paginator import CustomPagination
from api.products.product import tasks
from api.products.product.tasks import createCategories
from common.news.models import News


class NewsCreateAPIView(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAuthenticated]


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

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
        tasks.updateProducts.apply_async()
        createCategories()
        return queryset


class NewsDetailAPIView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class NewsUpdateAPIView(UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class NewsDeleteAPIView(DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
