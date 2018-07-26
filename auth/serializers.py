from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
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

    def validate(self, data):
        data = super().validate(data)
        namepass_provided = 'username' in data and 'password' in data
        if not namepass_provided:
            error = {'non_field_errors': ['Username with password should be provided']}
            raise ValidationError(detail=error)
        return data


class RefreshSerializer(Serializer):
    access_token = CharField(required=True)
    refresh_token = CharField(required=True)
