from django.urls import path

from api.banner.views import SmallBannerCreateAPIView, SmallBannerListAPIView, SmallBannerUpdateAPIView, \
    SmallBannerDeleteAPIView, BannerCreateAPIView, BannerListAPIView, BannerUpdateAPIView, BannerDeleteAPIView, \
    PointerNumberCreateAPIView, PointerNumberListAPIView, PointerNumberDetailAPIView

app_name = 'banner'

urlpatterns = [
    path("-create/", BannerCreateAPIView.as_view(), name="banner_create"),
    path("-list/", BannerListAPIView.as_view(), name="banner_list"),
    path("-update/<uuid:guid>/", BannerUpdateAPIView.as_view(), name="banner_update"),
    path("-destroy/<uuid:guid>/", BannerDeleteAPIView.as_view(), name="banner_delete"),

    path("-small-create/", SmallBannerCreateAPIView.as_view(), name="small_banner_create"),
    path("-small-list/", SmallBannerListAPIView.as_view(), name="small_banner_list"),
    path("-small-update/<uuid:guid>/", SmallBannerUpdateAPIView.as_view(), name="small_banner_update"),
    path("-small-destroy/<uuid:guid>/", SmallBannerDeleteAPIView.as_view(), name="small_banner_delete"),

    path("-number-create/", PointerNumberCreateAPIView.as_view(), name="number_create"),
    path("-number-list/", PointerNumberListAPIView.as_view(), name="number_list"),
    path("-number-update/<uuid:guid>/", PointerNumberDetailAPIView.as_view(), name="number_detail"),
]
