from rest_framework import serializers

from api.filial.serializers import FilialListSerializer
from common.social.models import Social


class SocialLinksSerializer(serializers.ModelSerializer):
    filials = serializers.SerializerMethodField()

    def get_filials(self, social):
        return FilialListSerializer(social.filial.all(), many=True).data

    class Meta:
        model = Social
        fields = ['id', 'guid', 'telegram', 'instagram', 'facebook', 'youtube', 'filials', 'phone']
