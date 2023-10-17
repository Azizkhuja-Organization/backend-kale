from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.portfolio.images.serializers import PortfolioImageCreateSerializer
from api.portfolio.serializers import PortfolioCreateSerializer, PortfolioDetailSerializer, PortfolioListSerializer, \
    PortfolioUpdateSerializer
from common.portfolio.models import Portfolio, PortfolioImage
from config.settings.base import CACHE_TTL


class PortfolioCreateAPIView(CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioCreateSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        photos = None
        if 'photos' in request.data:
            photos = request.data.pop('photos')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        portfolio = serializer.save()
        if photos:
            obj = []
            for photo in photos:
                serial = PortfolioImageCreateSerializer(data={
                    "portfolio": portfolio.id,
                    "photo": photo
                })
                serial.is_valid(raise_exception=True)
                obj.append(PortfolioImage(portfolio=portfolio, photo=serial.validated_data.get('photo')))
            if obj:
                PortfolioImage.objects.bulk_create(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PortfolioListAPIView(ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioListSerializer
    pagination_class = CustomPagination

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortfolioDetailAPIView(RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    lookup_field = 'guid'


class PortfolioUpdateAPIView(UpdateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        photos = request.data.pop('photos')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if photos:
            obj = []
            for photo in photos:
                serial = PortfolioImageCreateSerializer(data={
                    "portfolio": instance.id,
                    "photo": photo
                })
                serial.is_valid(raise_exception=True)
                obj.append(PortfolioImage(portfolio=instance, photo=serial.validated_data.get('photo')))
            if obj:
                PortfolioImage.objects.bulk_create(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortfolioDeleteAPIView(DestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
