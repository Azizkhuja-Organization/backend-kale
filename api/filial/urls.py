from django.urls import path
from api.filial.views import FilialCreateAPIView, FilialListAPIView, FilialDetailAPIView, \
    FilialUpdateAPIView, FilialDeleteAPIView

app_name = 'filial'

urlpatterns = [
    path("-create/", FilialCreateAPIView.as_view(), name="filial_create"),
    path("-list/", FilialListAPIView.as_view(), name="filial_list"),
    path("-detail/<uuid:guid>/", FilialDetailAPIView.as_view(), name="filial_detail"),
    path("-update/<uuid:guid>/", FilialUpdateAPIView.as_view(), name="filial_update"),
    path("-destroy/<uuid:guid>/", FilialDeleteAPIView.as_view(), name="filial_delete")
]
