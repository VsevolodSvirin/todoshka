from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CategoryPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser or obj.common or obj in request.user.categories.all()
        return request.user.is_superuser or not obj.common and obj in request.user.categories.all()

    def has_permission(self, request, view):
        return request.user.is_authenticated
