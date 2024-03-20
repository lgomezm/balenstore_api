from rest_framework.permissions import BasePermission, SAFE_METHODS
from items.models import Item, QuotationVisit
from users.models import UserType


class QuotationVisitEditPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == UserType.ADMINISTRATOR:
            return True
        if type(obj) == QuotationVisit:
            quotation_visit = obj
        elif type(obj) == Item:
            quotation_visit = obj.quotation_visit
        else:
            return False
        return quotation_visit.user == request.user and not self.__edits_status(
            request, quotation_visit
        )

    def __edits_status(self, request, quotation_visit):
        if request.method not in ["PUT", "PATCH"]:
            return False
        return (
            "status" in request.data
            and request.data["status"] != quotation_visit.status
        )
