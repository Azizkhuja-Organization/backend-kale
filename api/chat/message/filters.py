import django_filters
from rest_framework.filters import BaseFilterBackend

from common.chat.models import Message


class MessageFilter(django_filters.FilterSet):
    room_id = django_filters.NumberFilter(field_name='room__id')

    class Meta:
        model = Message
        fields = ['room_id']


class RoomFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        room_id = request.query_params.get('room_id')
        if room_id:
            queryset = queryset.filter(roomMessages=room_id)
        return queryset
