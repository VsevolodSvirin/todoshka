from django.urls import reverse
from rest_framework.test import APITestCase


class UserRegistrationAPITestCase(APITestCase):
    url = reverse('users:list')


class UserLoginAPITestCase(APITestCase):
    url = reverse('users:login')

    def test_auth_without_password(self):
        pass

    def test_auth_with_wrong_password(self):
        pass

    def test_auth_with_valid_data(self):
        pass
