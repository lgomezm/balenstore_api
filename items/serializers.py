from rest_framework import serializers

from items.models import Item, QuotationVisit


class QuotationVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationVisit
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
