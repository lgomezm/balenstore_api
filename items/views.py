import logging
import boto3
import mimetypes
import os
from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.utils import timezone
from balenstore import settings
from items.models import Item, QuotationVisit, QuotationVisitStatus
from items.permissions import QuotationVisitEditPermissions
from items.serializers import ItemSerializer, QuotationVisitSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import UserType


class QuotationVisitListCreateView(ListAPIView):
    serializer_class = QuotationVisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == UserType.ADMINISTRATOR:
            return QuotationVisit.objects.all()
        return QuotationVisit.objects.filter(user=self.request.user)

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

    def put(self, request, *args, **kwargs):
        self.__validate()
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.__validate()
        return super().patch(request, *args, **kwargs)

    def __validate(self):
        quotation_visit = self.get_object()
        if quotation_visit.status in [
            QuotationVisitStatus.APPROVED,
            QuotationVisitStatus.REJECTED,
        ]:
            raise ValidationError(
                "This quotation visit is already approved or rejected"
            )


class QuotationItemListCreateView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        id = self.__get_quotation_id()
        return Item.objects.filter(quotation_visit__id=id)

    def get(self, request, *args, **kwargs):
        id = self.__get_quotation_id()
        quotation_visit = get_object_or_404(QuotationVisit, id=id)
        if (
            quotation_visit.user != request.user
            and request.user.user_type != UserType.ADMINISTRATOR
        ):
            raise PermissionDenied(
                detail="You are not the owner of this quotation visit", code=403
            )
        return super().get(request, *args, **kwargs)

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

    def __get_quotation_id(self):
        match = resolve(self.request.path_info)
        return match.kwargs["quotation_item_pk"]


class QuotationItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [QuotationVisitEditPermissions]


class GenerateUploadUrl(APIView):
    def post(self, request):
        file_name = request.data["file_name"]
        _, file_ext = os.path.splitext(file_name)
        if file_ext not in mimetypes.types_map:
            return Response(
                {"error": f"Unsupported file extension: {file_ext}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        content_type = mimetypes.types_map[f"{file_ext}"]
        date = timezone.now().strftime("%Y_%m_%d_%H_%M_%S")
        key = f"{date}{file_ext}"
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        file_path = f"items/{key}"
        params = {
            "Bucket": settings.AWS_S3_BUCKET,
            "Key": file_path,
            "ContentType": content_type,
        }
        try:
            url = s3_client.generate_presigned_url(
                ClientMethod="put_object",
                Params=params,
                HttpMethod="put",
            )
            return Response(
                {
                    "url": url,
                    "final_url": f"{settings.AWS_CF_DIST_BASE_URL}{file_path}",
                },
                status=status.HTTP_200_OK,
            )
        except ClientError as e:
            logging.exception("Could not generate upload URL", e)
            return Response(
                {"error": "Could not generate upload URL"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
