from django.urls import path

from api.partner.views import PartnerCreateAPIView, PartnerListAPIView, PartnerDetailAPIView, \
    PartnerUpdateAPIView, PartnerDeleteAPIView

app_name = 'partner'

urlpatterns = [
    path("-create/", PartnerCreateAPIView.as_view(), name="partner_create"),
    path("-list/", PartnerListAPIView.as_view(), name="partner_list"),
    path("-detail/<uuid:guid>/", PartnerDetailAPIView.as_view(), name="partner_detail"),
    path("-update/<uuid:guid>/", PartnerUpdateAPIView.as_view(), name="partner_update"),
    path("-destroy/<uuid:guid>/", PartnerDeleteAPIView.as_view(), name="partner_delete"),
]
