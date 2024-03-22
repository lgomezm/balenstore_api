from django.urls import path

from auctions.views import (
    AuctionListView,
    ConvertQuotationVisitToAuctions,
    PlaceBidView,
)


urlpatterns = [
    path("convert", ConvertQuotationVisitToAuctions.as_view(), name="convert"),
    path("", AuctionListView.as_view(), name="list_auctions"),
    path("<int:pk>/bids", PlaceBidView.as_view(), name="list_auctions"),
]
