from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.banner.serializers import BannerCreateSerializer, BannerListSerializer, PointerNumberCreateSerializer, \
    SmallBannerCreateSerializer, SmallBannerListSerializer
from api.permissions import IsAdmin
from common.banner.models import Banner, PointerNumber, SmallBanner


class BannerCreateAPIView(CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCreateSerializer
    permission_classes = [IsAdmin]


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerListSerializer


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

    def list(self, request, *args, **kwargs):
        number = self.get_queryset().first()
        serializer = self.get_serializer(number)
        return Response(serializer.data)


class PointerNumberDetailAPIView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    queryset = PointerNumber.objects.all()
    serializer_class = PointerNumberCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
