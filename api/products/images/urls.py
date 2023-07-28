from django.urls import path

from api.products.images.views import ProductImageCreateAPIView, ProductImageListAPIView, ProductImageDetailAPIView, \
    ProductImageUpdateAPIView, ProductImageDeleteAPIView

app_name = 'productImage'

urlpatterns = [
    path("-create/", ProductImageCreateAPIView.as_view(), name="productImage_create"),
    path("-list/", ProductImageListAPIView.as_view(), name="productImage_list"),
    path("-detail/<uuid:guid>/", ProductImageDetailAPIView.as_view(), name="productImage_detail"),
    path("-update/<uuid:guid>/", ProductImageUpdateAPIView.as_view(), name="productImage_update"),
    path("-destroy/<uuid:guid>/", ProductImageDeleteAPIView.as_view(), name="productImage_delete"),
]
