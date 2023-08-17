from django.urls import path

from api.address.views import AddressCreateAPIView, AddressListAPIView, AddressDetailAPIView

app_name = 'address'

urlpatterns = [
    path("-create/", AddressCreateAPIView.as_view(), name="address_create"),
    path("-list/", AddressListAPIView.as_view(), name="address_list"),
    path("-detail/<uuid:guid>/", AddressDetailAPIView.as_view(), name="address_detail")
]
