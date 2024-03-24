from django.urls import path

from auctions.views import (
    AuctionListView,
    ConvertQuotationVisitToAuctions,
    ListCreateBidView,
)


urlpatterns = [
    path("convert", ConvertQuotationVisitToAuctions.as_view(), name="convert"),
    path("", AuctionListView.as_view(), name="list_auctions"),
    path("<int:auction_id>/bids", ListCreateBidView.as_view(), name="bids"),
]
