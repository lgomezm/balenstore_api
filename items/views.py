from django.urls import resolve
from items.models import Item, QuotationVisit, QuotationVisitStatus
from items.permissions import QuotationVisitEditPermissions
from items.serializers import ItemSerializer, QuotationVisitSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from users.auth_utils import OwnerPermissions, UserPermissions


class QuotationVisitListCreateView(ListAPIView):
    serializer_class = QuotationVisitSerializer
    queryset = QuotationVisit.objects.all()
    permission_classes = [UserPermissions]

    def post(self, request, *args, **kwargs):
        request.data.update(
            {"user": request.user.id, "status": QuotationVisitStatus.PENDING}
        )
        serializer = QuotationVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuotationVisitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuotationVisitSerializer
    queryset = QuotationVisit.objects.all()
    permission_classes = [QuotationVisitEditPermissions]


class QuotationItemListCreateView(ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        match = resolve(self.request.path_info)
        id = match.kwargs["quotation_item_pk"]
        return Item.objects.filter(quotation_visit__id=id)

    def post(self, request, *args, **kwargs):
        quotation_visit_id = self.kwargs["quotation_item_pk"]
        try:
            quotation_visit = QuotationVisit.objects.get(id=quotation_visit_id)
        except QuotationVisit.DoesNotExist:
            return Response(
                {"error": "Quotation visit not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if quotation_visit.user != request.user:
            return Response(
                {"error": "You are not the owner of this quotation visit"},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["quotation_visit"] = quotation_visit_id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuotationItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [QuotationVisitEditPermissions]
