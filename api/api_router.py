from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path('catalog', include("api.catalog.urls")),
    path('portfolio', include("api.portfolio.urls")),
    path('partner', include("api.partner.urls")),
    path('user', include("api.users.urls")),

    # CATEGORY
    path('category', include("api.products.category.urls")),
    path('subcategory', include("api.products.subcategory.urls")),

    # PRODUCT
    path('product', include("api.products.product.urls")),
    path('product-image', include("api.products.images.urls")),

    path('order', include("api.order.urls")),
    path('cart', include("api.cart.urls")),
    path('wishlist', include("api.wishlist.urls")),
    path('comparison', include("api.comparison.urls")),

    path('news', include("api.news.urls")),
    path('social', include("api.social.urls")),
    path('map', include("api.map.urls")),
    path('address', include("api.address.urls")),
    path('banner', include("api.banner.urls")),

    # PAYMENTS
    # path('payme', include("api.payment.payme.urls")),
    path('click', include("api.payment.click.urls")),
]
