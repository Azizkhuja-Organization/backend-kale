from rest_framework import serializers

from common.address.models import Address


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'guid', 'user', 'region', 'district', 'street', 'location']
