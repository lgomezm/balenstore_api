from rest_framework.permissions import BasePermission
from users.models import UserType


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == UserType.ADMINISTRATOR
        )


class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == UserType.USER


class OwnerPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.user_type == UserType.ADMINISTRATOR or obj.user == request.user
        )
