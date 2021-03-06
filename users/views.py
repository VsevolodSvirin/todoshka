from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsSelfOrAdmin
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]
