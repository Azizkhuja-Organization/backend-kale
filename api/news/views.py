from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.news.serializers import NewsCreateSerializer, NewsListSerializer, NewsDetailSerializer, NewsUpdateSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.news.models import News


class NewsCreateAPIView(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_actual = serializer.validated_data.get('isActual')
        if is_actual:
            News.objects.update(isActual=False)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by('-created_at')
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
        isActual = self.request.query_params.get('isActual')
        if isActual:
            queryset = queryset.filter(isActual=True)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class NewsDetailAPIView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    lookup_field = 'guid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewCount += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsUpdateAPIView(UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class NewsDeleteAPIView(DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
