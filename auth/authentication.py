from time import time

import jwt
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authentication import BaseAuthentication

from todoshka.settings import SECRET_KEY, JWT_LIFE_TIME


class JWTAuthentication(BaseAuthentication):
    # TODO Unit test dis shiet
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return None

        access_token = request.META.get('HTTP_AUTHORIZATION')

        user = get_user_by_jwt(access_token)

        if user is not None and user.is_active:
            return user, None
        return None

    def authenticate_header(self, request):
        endpoint = 'refresh' if 'HTTP_AUTHORIZATION' in request.META else 'login'
        return reverse('auth:{}'. format(endpoint))


def create_jwt(user_id, life_time=JWT_LIFE_TIME, secret_key=SECRET_KEY):
    now = time()
    payload = {
        'user_id': user_id,
        'iat': now,
        'exp': now + life_time,
    }

    return jwt.encode(payload, secret_key).decode()


def get_token_payload(token, secret_key=SECRET_KEY):
    split_token = token.split(maxsplit=1)

    if len(split_token) == 1:
        split_token = 'JWT', split_token[0]

    prefix, token = split_token

    if prefix.upper() != 'JWT':
        return None

    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None


def get_user_by_jwt(token):
    payload = get_token_payload(token)
    user_model = get_user_model()
    try:
        return user_model.objects.get(id=payload.get('user_id'))
    except (user_model.DoesNotExist, AttributeError):
        return None


def get_token_pair(user):
    return {
        'access_token': 'JWT ' + create_jwt(user.id),
        'refresh_token': 'trololo'
        # 'refresh_token': user.get_refresh_token()  # FIXME: implementation of refresh token in User model needed
    }
