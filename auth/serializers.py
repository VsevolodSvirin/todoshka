from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer, CharField


User = get_user_model()


class RegisterSerializer(Serializer):
    username = CharField(required=True)
    email = CharField(required=True)
    password = CharField(required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)
