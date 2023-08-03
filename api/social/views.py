from api.permissions import IsAdmin
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from api.social.serializers import SocialLinksSerializer
from common.social.models import Social


class SocialCreateAPIView(CreateAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAdmin]


class SocialListAPIView(ListAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAdmin]

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