from django.urls import path

from api.map.views import MapCreateAPIView, MapListAPIView, MapDetailAPIView, MapUpdateAPIView, MapDestroyAPIView

app_name = 'map'

urlpatterns = [
    path("-create/", MapCreateAPIView.as_view(), name="map_create"),
    path("-list/", MapListAPIView.as_view(), name="map_list"),
    path("-detail/<uuid:guid>/", MapDetailAPIView.as_view(), name="map_detail"),
    path("-update/<uuid:guid>/", MapUpdateAPIView.as_view(), name="map_update"),
    path("-destroy/<uuid:guid>/", MapDestroyAPIView.as_view(), name="map_destroy"),
]
