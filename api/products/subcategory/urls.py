from django.urls import path

from api.products.subcategory.views import SubCategoryCreateAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView, \
    SubCategoryUpdateAPIView, SubCategoryDeleteAPIView

app_name = 'subcategory'

urlpatterns = [
    path("-create/", SubCategoryCreateAPIView.as_view(), name="subcategory_create"),
    path("-list/", SubCategoryListAPIView.as_view(), name="subcategory_list"),
    path("-detail/<uuid:guid>/", SubCategoryDetailAPIView.as_view(), name="subcategory_detail"),
    path("-update/<uuid:guid>/", SubCategoryUpdateAPIView.as_view(), name="subcategory_update"),
    path("-destroy/<uuid:guid>/", SubCategoryDeleteAPIView.as_view(), name="subcategory_delete"),
]
