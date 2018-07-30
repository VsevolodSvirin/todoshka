from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from todolists.models import TodoList
from todolists.permissions import IsAuthorOrAdmin
from todolists.serializers import TodoListSerializer


class TodoListViewSet(ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]
