from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from categories.models import Category
from categories.permissions import CategoryPermissions
from categories.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]
