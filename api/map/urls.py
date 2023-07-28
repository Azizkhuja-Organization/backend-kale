from django.urls import path

from api.map.views import MapListAPIView, MapDetailAPIView

app_name = 'map'

urlpatterns = [
    path("-list/", MapListAPIView.as_view(), name="map_list"),
    path("-detail/<uuid:guid>/", MapDetailAPIView.as_view(), name="map_detail")
]
