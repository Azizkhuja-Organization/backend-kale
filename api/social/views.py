from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.social.serializers import SocialLinksSerializer
from common.social.models import Social
from config.settings.base import CACHE_TTL


class SocialCreateAPIView(CreateAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAdmin]


class SocialListAPIView(ListAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        socialLinks = self.queryset.first()

        return Response(SocialLinksSerializer(socialLinks).data)


class SocialDetailAPIView(RetrieveAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    lookup_field = 'guid'


class SocialUpdateAPIView(UpdateAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class SocialDeleteAPIView(DestroyAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
