from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth.authentication import get_token_pair

User = get_user_model()


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('auth:register')
        self.user_attrs = {
            'username': 'Cool Guy',
            'email': 'cool_guy@smedialink.com',
            'password': '123'
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.user_attrs)
        self.assertTrue(status.is_success(response.status_code))
        User.objects.get().delete()

    def test_missed_fields_fail(self):
        user_attrs_1 = {
            'username': 'Bad Guy',
            'email': 'bad_guy@smedialink.com',
        }
        user_attrs_2 = {
            'username': 'Bad Guy',
            'password': '321'
        }
        user_attrs_3 = {
            'email': 'bad_guy@smedialink.com',
            'password': '321'
        }

        response = self.client.post(self.url, user_attrs_1)
        self.assertTrue(status.is_client_error(response.status_code))

        response = self.client.post(self.url, user_attrs_2)
        self.assertTrue(status.is_client_error(response.status_code))

        response = self.client.post(self.url, user_attrs_3)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_user_already_exists_fail(self):
        self.client.post(self.url, self.user_attrs)
        response = self.client.post(self.url, self.user_attrs)
        self.assertTrue(status.is_client_error(response.status_code))


class LoginTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('auth:login')
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')

    def tearDown(self):
        self.user.delete()

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'Cool Guy', 'password': '123'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(set(response.data.keys()), {'user', 'access_token', 'refresh_token'})
        self.assertIn('id', response.data['user'])

    def test_missing_fields_failure(self):
        response = self.client.post(self.url, {'username': 'Bad Guy'})
        self.assertTrue(status.is_client_error(response.status_code))

        response = self.client.post(self.url, {'username': 'Bad Guy'})
        self.assertTrue(status.is_client_error(response.status_code))

    def test_login_fail_with_incorrect_user(self):
        response = self.client.post(self.url, {'username': 'Bad Guy', 'password': '321'})
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn('non_field_errors', response.data)

    def test_login_fail_with_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, {'username': 'Cool Guy', 'password': '123'})
        self.assertTrue(status.is_client_error(response.status_code))


class RefreshTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('auth:refresh')
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.tokens = get_token_pair(self.user)

    def tearDown(self):
        self.user.delete()

    def test_refresh_success(self):
        response = self.client.post(self.url, self.tokens)
        self.assertTrue(status.is_success(response.status_code))

    def test_refresh_failure(self):
        access_token_missing = {'refresh_token': self.tokens['refresh_token']}
        response = self.client.post(self.url, access_token_missing)
        self.assertTrue(status.is_client_error(response.status_code))

        refresh_token_missing = {'access_token': self.tokens['access_token']}
        response = self.client.post(self.url, refresh_token_missing)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_token_is_invalid(self):
        wrong_refresh_token = {'access_token': self.tokens['access_token'],
                               'refresh_token': 'This is a token, trust me!'}
        response = self.client.post(self.url, wrong_refresh_token)
        self.assertTrue(status.is_client_error(response.status_code))
