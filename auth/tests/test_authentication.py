import time

from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.test import APIClient

from auth.authentication import get_user_by_jwt, create_jwt, get_token_pair
from users.models import User


class JWTAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Cool Guy', email='cool_guy@smedialink.com', password='123')

    def test_get_user_by_access_token(self):
        jwt = create_jwt(self.user.id)
        user = get_user_by_jwt(jwt)

        self.assertEqual(user, self.user)

    def test_token_expired(self):
        token = create_jwt(self.user.id, life_time=0)
        time.sleep(1)
        user = get_user_by_jwt(token)
        self.assertIsNone(user)

    def test_get_token_pair(self):
        tokens = get_token_pair(self.user)

        self.assertIn('access_token', tokens)
        self.assertIn('refresh_token', tokens)
        self.assertIn('JWT ', tokens['access_token'])

    def test_login(self):
        url = reverse('auth:login')

        r = self.client.post(url, {'username': 'Bad Guy', 'password': '321'})
        self.assertEqual(r.status_code, HTTP_404_NOT_FOUND)
        self.assertIn('non_field_errors', r.data)

        r = self.client.post(url, {'username': 'Cool Guy', 'password': '123'})
        self.assertEqual(r.status_code, HTTP_200_OK)
        self.assertEqual(set(r.data.keys()), {'user', 'access_token', 'refresh_token'})
        self.assertIn('id', r.data['user'])

        self.user.is_active = False
        self.user.save()
        r = self.client.post(url, {'username': 'Cool Guy', 'password': '123'})
        self.assertEqual(r.status_code, HTTP_404_NOT_FOUND)

    def test_refresh(self):
        # tokens = get_token_pair(self.user)

        assert False
