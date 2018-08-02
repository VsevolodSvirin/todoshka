from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.author_id == request.user.pk

    def has_permission(self, request, view):
        return request.user.is_authenticated
