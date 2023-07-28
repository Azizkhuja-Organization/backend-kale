from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.auth.views import LogoutView, SignInAPIView, SignUpAPIView, ReSendCodeAPIView, VerifyCodeAPIview

urlpatterns = [
    path('logout/', LogoutView.as_view(), name="logout"),
    path('sign_in/', SignInAPIView.as_view(), name='sign_in'),
    path('sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('verify/', VerifyCodeAPIview.as_view(), name='verify'),
    path('resend_code/', ReSendCodeAPIView.as_view(), name='resend_code'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
