from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.partner.serializers import PartnerCreateSerializer, PartnerListSerializer, PartnerDetailSerializer
from api.permissions import IsAdmin
from common.partner.models import Partner
from config.settings.base import CACHE_TTL


class PartnerCreateAPIView(CreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]


class PartnerListAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerListSerializer
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


class PartnerDetailAPIView(RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    lookup_field = 'guid'


class PartnerUpdateAPIView(UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class PartnerDeleteAPIView(DestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
