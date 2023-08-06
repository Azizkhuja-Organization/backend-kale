from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.portfolio.serializers import PortfolioCreateSerializer, PortfolioDetailSerializer, PortfolioListSerializer
from common.portfolio.models import Portfolio


class PortfolioCreateAPIView(CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioCreateSerializer
    permission_classes = [IsAdmin]


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


class PortfolioDeleteAPIView(DestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
