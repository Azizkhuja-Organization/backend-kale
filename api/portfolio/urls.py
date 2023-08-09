from django.urls import path

from api.portfolio.images.views import PortfolioImageCreateAPIView, PortfolioImageListAPIView, \
    PortfolioImageDetailAPIView, PortfolioImageUpdateAPIView, PortfolioImageDeleteAPIView
from api.portfolio.views import PortfolioCreateAPIView, PortfolioListAPIView, PortfolioDetailAPIView, \
    PortfolioUpdateAPIView, PortfolioDeleteAPIView

app_name = 'portfolio'

urlpatterns = [
    path("-create/", PortfolioCreateAPIView.as_view(), name="portfolio_create"),
    path("-list/", PortfolioListAPIView.as_view(), name="portfolio_list"),
    path("-detail/<uuid:guid>/", PortfolioDetailAPIView.as_view(), name="portfolio_detail"),
    path("-update/<uuid:guid>/", PortfolioUpdateAPIView.as_view(), name="portfolio_update"),
    path("-destroy/<uuid:guid>/", PortfolioDeleteAPIView.as_view(), name="portfolio_delete"),

    path("-image-create/", PortfolioImageCreateAPIView.as_view(), name="portfolioImage_create"),
    path("-image-list/", PortfolioImageListAPIView.as_view(), name="portfolioImage_list"),
    path("-image-detail/<uuid:guid>/", PortfolioImageDetailAPIView.as_view(), name="portfolioImage_detail"),
    path("-image-update/<uuid:guid>/", PortfolioImageUpdateAPIView.as_view(), name="portfolioImage_update"),
    path("-image-destroy/<uuid:guid>/", PortfolioImageDeleteAPIView.as_view(), name="portfolioImage_delete"),
]
