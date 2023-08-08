from django.urls import path

from api.wishlist.views import WishlistAddSubAPIView, WishlistProductsAPIView

app_name = 'wishlist'

urlpatterns = [
    path('-products/', WishlistProductsAPIView.as_view(), name='wishlist-products'),
    path('-action/', WishlistAddSubAPIView.as_view(), name='wishlist-add-sub'),
]
