from django.urls import path

from api.products.category.views import CategoryCreateAPIView, CategoryListAPIView, CategoryDetailAPIView, \
    CategoryUpdateAPIView, CategoryDeleteAPIView

app_name = 'category'

urlpatterns = [
    path("-create/", CategoryCreateAPIView.as_view(), name="category_create"),
    path("-list/", CategoryListAPIView.as_view(), name="category_list"),
    path("-detail/<uuid:guid>/", CategoryDetailAPIView.as_view(), name="category_detail"),
    path("-update/<uuid:guid>/", CategoryUpdateAPIView.as_view(), name="category_update"),
    path("-destroy/<uuid:guid>/", CategoryDeleteAPIView.as_view(), name="category_delete"),
]
