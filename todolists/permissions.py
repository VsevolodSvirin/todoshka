from rest_framework import permissions
from rest_framework.permissions import BasePermission


class TodoListsPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser or request.user.pk in [obj.author.pk, obj.assignee.pk]
        return request.user.is_superuser or request.user.pk == obj.author.pk

    def has_permission(self, request, view):
        return request.user.is_authenticated
