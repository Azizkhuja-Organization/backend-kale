from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.portfolio.images.serializers import PortfolioImageCreateSerializer, PortfolioImageListSerializer, \
    PortfolioImageDetailSerializer
from common.portfolio.models import PortfolioImage


class PortfolioImageCreateAPIView(CreateAPIView):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageCreateSerializer
    permission_classes = [IsAdmin]


class PortfolioImageListAPIView(ListAPIView):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class PortfolioImageDetailAPIView(RetrieveAPIView):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageDetailSerializer
    lookup_field = 'guid'


class PortfolioImageUpdateAPIView(UpdateAPIView):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class PortfolioImageDeleteAPIView(DestroyAPIView):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
