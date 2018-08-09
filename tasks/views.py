from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.permissions import TasksPermissions
from tasks.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TasksPermissions]
