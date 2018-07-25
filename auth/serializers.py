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
    token = CharField(required=False)

    def get_fields(self):
        fields = super().get_fields()
        if 'token' in self.initial_data:
            fields['token'].required = True
            fields['username'].required = False
            fields['password'].required = False
        return fields

    def validate(self, data):
        data = super().validate(data)
        token_provided = 'token' in data
        namepass_provided = 'username' in data and 'password' in data
        if token_provided and namepass_provided:
            error = {'non_field_errors': ['Only token or username with password should be provided']}
            raise ValidationError(detail=error)
        if not token_provided and not namepass_provided:
            error = {'non_field_errors': ['Token or username with password should be provided']}
            raise ValidationError(detail=error)
        return data
