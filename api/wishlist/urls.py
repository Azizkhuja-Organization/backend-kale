from django.urls import path

from api.wishlist.views import WishlistCreateAPIView, WishlistListAPIView, WishlistDetailAPIView, \
    WishlistUpdateAPIView, WishlistAddSubAPIView, WishlistProductsAPIView

app_name = 'wishlist'

urlpatterns = [
    # path("-create/", WishlistCreateAPIView.as_view(), name="wishlist_create"),
    # path("-list/", WishlistListAPIView.as_view(), name="wishlist_list"),
    # path("-detail/<uuid:guid>/", WishlistDetailAPIView.as_view(), name="wishlist_detail"),
    # path("-update/<uuid:guid>/", WishlistUpdateAPIView.as_view(), name="wishlist_update"),

    path('-products/', WishlistProductsAPIView.as_view(), name='wishlist-products'),
    path('-action/', WishlistAddSubAPIView.as_view(), name='wishlist-add-sub'),
]
