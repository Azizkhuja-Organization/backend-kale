from django.urls import path

from api.cart.views import CartCreateAPIView, CartAddSubAPIView, CartProductListAPIView, CartProductDestroyAPIView, \
    CountersAPIView

app_name = 'cart'

urlpatterns = [
    path("-create/", CartCreateAPIView.as_view(), name="cart_create"),
    path("-products/", CartProductListAPIView.as_view(), name="cart_list"),
    path("-destroy/<uuid:guid>/", CartProductDestroyAPIView.as_view(), name="cart_destroy"),

    path('-action/', CartAddSubAPIView.as_view(), name='cart-add-sub'),
    path('-counters/', CountersAPIView.as_view(), name='counters'),
]
