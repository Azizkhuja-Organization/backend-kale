from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.filial.serializers import FilialCreateSerializer, FilialListSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.social.models import Filial


class FilialCreateAPIView(CreateAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialCreateSerializer
    permission_classes = [IsAdmin]


class FilialListAPIView(ListAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialListSerializer

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


class FilialDetailAPIView(RetrieveAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialCreateSerializer
    lookup_field = 'guid'


class FilialUpdateAPIView(UpdateAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class FilialDeleteAPIView(DestroyAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
