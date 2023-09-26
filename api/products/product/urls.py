from django.urls import path

from api.products.product.views import ProductCreateAPIView, ProductListAPIView, ProductDetailAPIView, \
    ProductUpdateAPIView, ProductDeleteAPIView, ProductUpdatesAPIView

app_name = 'product'

urlpatterns = [
    path("-create/", ProductCreateAPIView.as_view(), name="product_create"),
    path("-list/", ProductListAPIView.as_view(), name="product_list"),
    path("-updates/", ProductUpdatesAPIView.as_view(), name="product_updates"),
    path("-detail/<uuid:guid>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("-update/<uuid:guid>/", ProductUpdateAPIView.as_view(), name="product_update"),
    path("-destroy/<uuid:guid>/", ProductDeleteAPIView.as_view(), name="product_delete"),
]

