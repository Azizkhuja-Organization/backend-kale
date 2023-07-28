from django.urls import path

from . import views as _views

app_name = 'message'

urlpatterns = [
    path('-create/', _views.MessageCreateAPIView.as_view(), name='message_create'),
    path('-list/', _views.MessageListAPIView.as_view(), name='message_list'),
    path('-detail/<uuid:guid>/', _views.MessageDetailAPIView.as_view(), name='message_detail'),
]
