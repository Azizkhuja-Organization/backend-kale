from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.portfolio.images.serializers import PortfolioImageCreateSerializer
from api.portfolio.serializers import PortfolioCreateSerializer, PortfolioDetailSerializer, PortfolioListSerializer
from common.portfolio.models import Portfolio, PortfolioImage


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
        return queryset


class PortfolioDetailAPIView(RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    lookup_field = 'guid'


class PortfolioUpdateAPIView(UpdateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioCreateSerializer
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
