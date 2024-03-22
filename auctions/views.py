from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from auctions.models import Auction
from auctions.serializers import AuctionSerializer, ConvertToAuctionsSerializer


class ConvertQuotationVisitToAuctions(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ConvertToAuctionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.data.get("items")
        auctions = []
        with transaction.atomic():
            for item in items:
                auction = Auction.objects.create(
                    item_id=item.get("item_id"),
                    starting_bid=item.get("starting_bid"),
                    closes_at=item.get("closes_at"),
                )
                auctions.append(auction)
        response_serializer = AuctionSerializer(auctions, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
