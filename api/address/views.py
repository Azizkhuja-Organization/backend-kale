from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.address.serializers import AddressCreateSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin, IsClient
from common.address.models import Address
from common.users.models import User


class AddressCreateAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer
    permission_classes = [IsAdmin | IsClient]


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.all().order_by('-created_at')
    serializer_class = AddressCreateSerializer
    permission_classes = [IsAdmin | IsClient]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.UserRole.CLIENT:
            queryset = queryset.filter(user=self.request.user)

        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class AddressDetailAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer
    permission_classes = [IsAdmin | IsClient]
    lookup_field = 'guid'
