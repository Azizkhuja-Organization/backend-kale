from django.urls import path

from .views import PaymentClick, PaymentPrepareAPIView, PaymentCompleteAPIView

urlpatterns = [
    # path('-prepare/', prepare, name='prepare'),
    # path('-complete/', complete, name='complete'),
    # path('-service/<service_type>/', service, name='service'),

    path('-prepare/', PaymentPrepareAPIView.as_view(), name='click_prepare'),
    path('-complete/', PaymentCompleteAPIView.as_view(), name='click_complete'),
    path('-pay/', PaymentClick.as_view(), name='click_payment'),
    # path('-complete/', PaymentComplate.as_view(), name='click_complete'),

]
