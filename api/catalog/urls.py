from django.urls import path
from api.catalog.views import CatalogCreateAPIView, CatalogListAPIView, CatalogDetailAPIView, \
    CatalogUpdateAPIView, CatalogDeleteAPIView

app_name = 'catalog'

urlpatterns = [
    path("-create/", CatalogCreateAPIView.as_view(), name="catalog_create"),
    path("-list/", CatalogListAPIView.as_view(), name="catalog_list"),
    path("-detail/<uuid:guid>/", CatalogDetailAPIView.as_view(), name="catalog_detail"),
    path("-update/<uuid:guid>/", CatalogUpdateAPIView.as_view(), name="catalog_update"),
    path("-destroy/<uuid:guid>/", CatalogDeleteAPIView.as_view(), name="catalog_delete")
]
