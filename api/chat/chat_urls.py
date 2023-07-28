from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "chat"
urlpatterns = router.urls
urlpatterns += [
    path('message', include("api.chat.message.urls", namespace='message')),
    path('room', include("api.chat.room.urls", namespace='room')),
]
