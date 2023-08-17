from django.urls import path

from api.order.views import OrderListAPIView, OrderDetailAPIView, OrderUpdateAPIView, OrderCreateAPIView, \
    OrderDeleteAPIView

app_name = 'order'

urlpatterns = [
    path("-create/", OrderCreateAPIView.as_view(), name="order_create"),
    path("-list/", OrderListAPIView.as_view(), name="order_list"),
    path("-detail/<uuid:guid>/", OrderDetailAPIView.as_view(), name="order_detail"),
    path("-update/<uuid:guid>/", OrderUpdateAPIView.as_view(), name="order_update"),
    path("-destroy/<uuid:guid>/", OrderDeleteAPIView.as_view(), name="order_delete"),
]
