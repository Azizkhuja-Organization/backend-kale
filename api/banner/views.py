from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.banner.serializers import BannerCreateSerializer, BannerListSerializer, PointerNumberCreateSerializer, \
    SmallBannerCreateSerializer, SmallBannerListSerializer, HeaderDiscountCreateSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.banner.models import Banner, PointerNumber, SmallBanner, HeaderDiscount


class BannerCreateAPIView(CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCreateSerializer
    permission_classes = [IsAdmin]


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerListSerializer
    pagination_class = CustomPagination

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    # def list(self, request, *args, **kwargs):
    #     return super().list(self, request, *args, **kwargs)


class BannerUpdateAPIView(UpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class BannerDeleteAPIView(DestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class SmallBannerCreateAPIView(CreateAPIView):
    queryset = SmallBanner.objects.all()
    serializer_class = SmallBannerCreateSerializer
    permission_classes = [IsAdmin]


class SmallBannerListAPIView(ListAPIView):
    queryset = SmallBanner.objects.all()
    serializer_class = SmallBannerListSerializer
    pagination_class = CustomPagination

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SmallBannerUpdateAPIView(UpdateAPIView):
    queryset = SmallBanner.objects.all()
    serializer_class = SmallBannerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class SmallBannerDeleteAPIView(DestroyAPIView):
    queryset = SmallBanner.objects.all()
    serializer_class = SmallBannerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class PointerNumberCreateAPIView(CreateAPIView):
    queryset = PointerNumber.objects.all()
    serializer_class = PointerNumberCreateSerializer
    permission_classes = [IsAdmin]


class PointerNumberListAPIView(ListAPIView):
    queryset = PointerNumber.objects.all()
    serializer_class = PointerNumberCreateSerializer

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        number = self.get_queryset().first()
        serializer = self.get_serializer(number)
        return Response(serializer.data)


class PointerNumberDetailAPIView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    queryset = PointerNumber.objects.all()
    serializer_class = PointerNumberCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class HeaderDiscountDetailAPIView(ModelViewSet):
    queryset = HeaderDiscount.objects.all().order_by('-enabled')
    serializer_class = HeaderDiscountCreateSerializer
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(enabled=True)
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        else:
            return Response(status=404)
