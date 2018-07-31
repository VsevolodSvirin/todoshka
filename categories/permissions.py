from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return request.user.is_superuser or not obj.common and obj.user_id and obj.user_id == request.user.pk
        return request.user.is_superuser or obj.common or obj.user_id and obj.user_id == request.user.pk

    def has_permission(self, request, view):
        return request.user.is_authenticated
