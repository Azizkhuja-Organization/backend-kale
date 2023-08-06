from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView

from api.chat.room import serializers as _serializers
from common.chat.models import Room


# MESSAGES
class RoomCreateAPIView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = _serializers.RoomSerializer
    # permission_classes = [IsAuthenticated]


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = _serializers.RoomSerializer
    # permission_classes = [IsAuthenticated]


class RoomDetailAPIView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = _serializers.RoomSerializer
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'guid'


class RoomUpdateAPIView(UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = _serializers.RoomSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'


class RoomDestroyAPIView(DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = _serializers.RoomSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
