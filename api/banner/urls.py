from django.urls import path

from api.news.views import NewsCreateAPIView, NewsListAPIView, NewsDetailAPIView, \
    NewsUpdateAPIView, NewsDeleteAPIView

app_name = 'news'

urlpatterns = [
    path("-create/", NewsCreateAPIView.as_view(), name="news_create"),
    path("-list/", NewsListAPIView.as_view(), name="news_list"),
    path("-detail/<uuid:guid>/", NewsDetailAPIView.as_view(), name="news_detail"),
    path("-update/<uuid:guid>/", NewsUpdateAPIView.as_view(), name="news_update"),
    path("-destroy/<uuid:guid>/", NewsDeleteAPIView.as_view(), name="news_delete"),
]
