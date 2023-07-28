from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.social.serializers import SocialLinksSerializer
from common.social.models import Social


class SocialListAPIView(ListAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer

    def list(self, request, *args, **kwargs):
        socialLinks = self.queryset.first()
        return Response(SocialLinksSerializer(socialLinks).data)
