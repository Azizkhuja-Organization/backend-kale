from django.urls import path

from api.comparison.views import ComparisonAddSubAPIView, ComparisonProductsAPIView

app_name = 'comparison'

urlpatterns = [
    path('-products/', ComparisonProductsAPIView.as_view(), name='comparison-products'),
    path('-action/', ComparisonAddSubAPIView.as_view(), name='comparison-add-sub'),
]
