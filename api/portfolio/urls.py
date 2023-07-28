from django.urls import path

from api.portfolio.views import PortfolioCreateAPIView, PortfolioListAPIView, PortfolioDetailAPIView, \
    PortfolioUpdateAPIView, PortfolioDeleteAPIView

app_name = 'portfolio'

urlpatterns = [
    path("-create/", PortfolioCreateAPIView.as_view(), name="portfolio_create"),
    path("-list/", PortfolioListAPIView.as_view(), name="portfolio_list"),
    path("-detail/<uuid:guid>/", PortfolioDetailAPIView.as_view(), name="portfolio_detail"),
    path("-update/<uuid:guid>/", PortfolioUpdateAPIView.as_view(), name="portfolio_update"),
    path("-destroy/<uuid:guid>/", PortfolioDeleteAPIView.as_view(), name="portfolio_delete"),
]
