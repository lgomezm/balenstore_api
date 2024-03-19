from items.models import QuotationVisit, QuotationVisitStatus
from items.serializers import QuotationVisitSerializer
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
    permission_classes = [OwnerPermissions]
