from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.pk == request.user.pk

    def has_permission(self, request, view):
        return request.user.is_authenticated
