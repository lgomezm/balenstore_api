from django.db import transaction
from django.db.models import Max
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from auctions.models import Auction, Bid
from auctions.serializers import (
    AuctionSerializer,
    BidSerializer,
    ConvertToAuctionsSerializer,
    PlaceBidSerializer,
)
from users.auth_utils import AdminPermissions
from django.utils import timezone


class ConvertQuotationVisitToAuctions(GenericAPIView):
    permission_classes = [AdminPermissions]

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


class AuctionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()


class PlaceBidView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = PlaceBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return Response(
                {"error": "Auction does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if auction.closes_at < timezone.now():
            return Response(
                {"error": "Auction is already closed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        max_bid = Bid.objects.filter(auction=auction).aggregate(Max("amount"))[
            "amount__max"
        ]
        if not max_bid:
            if serializer.data.get("bid") <= auction.starting_bid:
                return Response(
                    {"error": "Bid amount must be greater than the starting bid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif serializer.data.get("bid") <= max_bid:
            return Response(
                {"error": "Bid amount must be greater than the current bid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        bid = Bid.objects.create(
            auction_id=pk,
            bidder=request.user,
            amount=serializer.data.get("bid"),
        )
        response_serializer = BidSerializer(bid)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
