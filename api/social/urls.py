from django.urls import path

from api.social.views import SocialListAPIView

app_name = 'social'

urlpatterns = [
    path("-list/", SocialListAPIView.as_view(), name="social_list"),
]
