from django.urls import path

from api.address.views import AddressCreateAPIView, AddressListAPIView, AddressDetailAPIView, RegionViewSet, \
    DistrictViewSet, StreetViewSet

app_name = 'address'

urlpatterns = [
    path("-create/", AddressCreateAPIView.as_view(), name="address_create"),
    path("-list/", AddressListAPIView.as_view(), name="address_list"),
    path("-regions/", RegionViewSet.as_view(), name="region_list"),
    path("-distcricts/", DistrictViewSet.as_view(), name="district_list"),
    path("-streets/", StreetViewSet.as_view(), name="street_list"),
    path("-detail/<uuid:guid>/", AddressDetailAPIView.as_view(), name="address_detail")
]
