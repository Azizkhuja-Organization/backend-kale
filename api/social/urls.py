from django.urls import path

from api.social.views import SocialCreateAPIView, SocialDeleteAPIView, SocialDetailAPIView, SocialListAPIView, \
    SocialUpdateAPIView

app_name = 'social'

urlpatterns = [
    path("-create/", SocialCreateAPIView.as_view(), name="social_create"),
    path("-list/", SocialListAPIView.as_view(), name="social_list"),
    path("-detail/<uuid:guid>/", SocialDetailAPIView.as_view(), name="social_detail"),
    path("-update/<uuid:guid>/", SocialUpdateAPIView.as_view(), name="social_update"),
    path("-destroy/<uuid:guid>/", SocialDeleteAPIView.as_view(), name="social_delete"),
]
