from django.urls import path

from auctions.views import ConvertQuotationVisitToAuctions


urlpatterns = [
    path("convert", ConvertQuotationVisitToAuctions.as_view(), name="convert"),
]
