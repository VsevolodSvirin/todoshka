from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from auth.authentication import get_user_by_jwt, create_jwt, get_token_pair, JWTAuthentication

User = get_user_model()


class JWTAuthenticationTestCase(TestCase):
    def setUp(self):
        self.auth_service = JWTAuthentication()
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.tokens = get_token_pair(self.user)

    def tearDown(self):
        self.user.delete()

    def test_authenticate(self):
        request = Mock()
        request.META = {}
        user = self.auth_service.authenticate(request)

        self.assertIsNone(user)

        request.META['HTTP_AUTHORIZATION'] = self.tokens['access_token']
        user, auth = self.auth_service.authenticate(request)

        self.assertEqual(user, get_user_by_jwt(token=self.tokens['access_token']))
        self.assertEqual(auth, None)

        request.META['HTTP_AUTHORIZATION'] = 'Trust me, this is a token!'
        user = self.auth_service.authenticate(request)

        self.assertIsNone(user, get_user_by_jwt(token=self.tokens['access_token']))

    def test_authenticate_header(self):
        request = Mock()
        request.META = {}
        endpoint = self.auth_service.authenticate_header(request)

        self.assertEqual(endpoint, reverse('auth:login'))

        request.META['HTTP_AUTHORIZATION'] = self.tokens['access_token']
        endpoint = self.auth_service.authenticate_header(request)

        self.assertEqual(endpoint, reverse('auth:refresh'))


class TokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')

    def tearDown(self):
        self.user.delete()

    def test_get_user_by_access_token(self):
        jwt = create_jwt(self.user.id)
        user = get_user_by_jwt(jwt)

        self.assertEqual(user, self.user)

    def test_token_expired(self):
        token = create_jwt(self.user.id, life_time=-1)
        user = get_user_by_jwt(token)
        self.assertIsNone(user)

    def test_get_token_pair(self):
        tokens = get_token_pair(self.user)

        self.assertIn('access_token', tokens)
        self.assertIn('refresh_token', tokens)
        self.assertIn('JWT ', tokens['access_token'])
