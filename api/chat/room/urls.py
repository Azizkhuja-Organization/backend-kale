from django.urls import path

from . import views as _views

app_name = 'room'

urlpatterns = [
    path('-create/', _views.RoomCreateAPIView.as_view(), name='room_create'),
    path('-list/', _views.RoomListAPIView.as_view(), name='room_detail'),
    path('-detail/<uuid:guid>/', _views.RoomDetailAPIView.as_view(), name='room_detail'),
    path('-update/<uuid:guid>/', _views.RoomUpdateAPIView.as_view(), name='room_detail'),
    path('-destroy/<uuid:guid>/', _views.RoomDestroyAPIView.as_view(), name='room_detail')
]
