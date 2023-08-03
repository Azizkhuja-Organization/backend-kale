from django.urls import path

from api.cart.views import CartAddSubAPIView, CartProductListAPIView, CartProductDestroyAPIView, \
    CountersAPIView

app_name = 'cart'

urlpatterns = [
    path("-products/", CartProductListAPIView.as_view(), name="cart_product_list"),
    path("-destroy/<uuid:guid>/", CartProductDestroyAPIView.as_view(), name="cart_product_destroy"),

    path('-action/', CartAddSubAPIView.as_view(), name='cart-add-sub'),
    path('-counters/', CountersAPIView.as_view(), name='counters'),
]
