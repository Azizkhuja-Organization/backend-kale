from rest_framework import serializers

from common.social.models import Social


class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['telegram', 'instagram', 'facebook', 'youtube', 'phone', 'location']
