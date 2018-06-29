from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.models import TodoList
from api.permissions import IsAuthorOrAdmin
from api.serializers import TodoListSerializer


class TodoListViewSet(ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]


router = DefaultRouter()
router.register(r'todolists', TodoListViewSet)
