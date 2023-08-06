from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from common.chat.models import Message
from . import serializers as _serializers
from .filters import RoomFilterBackend
from ...paginator import CustomPagination


class MessageCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = _serializers.MessageCreateSerializer
    # permission_classes = [IsAuthenticated]


class MessageListAPIView(ListAPIView):
    queryset = Message.objects.select_related('sender').all()
    serializer_class = _serializers.MessageListSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [RoomFilterBackend]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(content__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class MessageDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.select_related('sender').all()
    serializer_class = _serializers.MessageListSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'guid'
