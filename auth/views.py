from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.authentication import get_token_pair, get_token_payload
from auth.serializers import RegisterSerializer, LoginSerializer, RefreshSerializer
from users.serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request, **kwargs):
        serialized_request = RegisterSerializer(data=request.data)
        if not serialized_request.is_valid():
            return Response(serialized_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(username=serialized_request.validated_data['username']).exists():
            serialized_request.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serialized_request.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, **kwargs):
        serialized_request = LoginSerializer(data=request.data)
        if not serialized_request.is_valid():
            return Response(serialized_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=serialized_request.data['username'], is_active=True).first()
        if not user or not user.check_password(serialized_request.data['password']):
            return Response(
                {'non_field_errors': ['Wrong username or password']},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({'user': UserSerializer(user).data, **get_token_pair(user)})


class RefreshView(APIView):
    def post(self, request, **kwargs):
        serialized_request = RefreshSerializer(data=request.data)
        if not serialized_request.is_valid():
            return Response(serialized_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        access_token_payload = get_token_payload(serialized_request.data['access_token'])
        refresh_token = serialized_request.data['refresh_token']
        user = User.objects.filter(id=access_token_payload['user_id']).first()
        actual_refresh_token = user.refresh_token

        if actual_refresh_token != refresh_token:
            return Response(
                {'non_field_errors': ['Wrong token pair']},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.update_refresh_token()
        return Response({'user': UserSerializer(user).data, **get_token_pair(user)})
