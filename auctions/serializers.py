from decimal import Decimal
from django.http import Http404
from django.utils import timezone
from rest_framework import serializers

from auctions.models import Auction, Bid
from items.models import Item, QuotationVisit
from items.serializers import ItemSerializer


class ItemToAuctionSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    starting_bid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal(1),
    )
    closes_at = serializers.DateTimeField()


class ConvertToAuctionsSerializer(serializers.Serializer):
    quotation_visit_id = serializers.IntegerField()
    items = serializers.ListField(child=ItemToAuctionSerializer())

    def validate(self, data):
        visit_id = data.get("quotation_visit_id")
        try:
            QuotationVisit.objects.get(id=visit_id)
        except QuotationVisit.DoesNotExist:
            raise Http404("No QuotationVisit matches the given id.")

        items = Item.objects.filter(quotation_visit=visit_id)
        existing_item_ids = {item.id for item in items}
        item_ids = {item.get("item_id") for item in data.get("items")}
        missing_item_ids = existing_item_ids - item_ids
        if missing_item_ids:
            raise serializers.ValidationError(
                f"Item ids {missing_item_ids} must be provided."
            )

        for item in data.get("items"):
            if item.get("closes_at") <= timezone.now():
                raise serializers.ValidationError(
                    f"Auction for item {item.get('item_id')} can't close in the past."
                )

        return super().validate(data)


class AuctionSerializer(serializers.ModelSerializer):
    item_data = ItemSerializer(source="item", read_only=True)

    class Meta:
        model = Auction
        fields = "__all__"


class PlaceBidSerializer(serializers.Serializer):
    bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(1)
    )


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"
