from django.urls import path

from api.catalog.images.views import CatalogImageCreateAPIView, CatalogImageListAPIView, CatalogImageDetailAPIView, \
    CatalogImageUpdateAPIView, CatalogImageDeleteAPIView
from api.catalog.views import CatalogCreateAPIView, CatalogListAPIView, CatalogDetailAPIView, \
    CatalogUpdateAPIView, CatalogDeleteAPIView

app_name = 'catalog'

urlpatterns = [
    path("-create/", CatalogCreateAPIView.as_view(), name="catalog_create"),
    path("-list/", CatalogListAPIView.as_view(), name="catalog_list"),
    path("-detail/<uuid:guid>/", CatalogDetailAPIView.as_view(), name="catalog_detail"),
    path("-update/<uuid:guid>/", CatalogUpdateAPIView.as_view(), name="catalog_update"),
    path("-destroy/<uuid:guid>/", CatalogDeleteAPIView.as_view(), name="catalog_delete"),

    path("-image-create/", CatalogImageCreateAPIView.as_view(), name="catalogImage_create"),
    path("-image-list/", CatalogImageListAPIView.as_view(), name="catalogImage_list"),
    path("-image-detail/<uuid:guid>/", CatalogImageDetailAPIView.as_view(), name="catalogImage_detail"),
    path("-image-update/<uuid:guid>/", CatalogImageUpdateAPIView.as_view(), name="catalogImage_update"),
    path("-image-destroy/<uuid:guid>/", CatalogImageDeleteAPIView.as_view(), name="catalogImage_delete"),
]
