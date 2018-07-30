from django.contrib.auth import get_user_model
from django.test import TestCase

from auth.authentication import get_user_by_jwt, create_jwt, get_token_pair

User = get_user_model()


class JWTAuthenticationTestCase(TestCase):
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
