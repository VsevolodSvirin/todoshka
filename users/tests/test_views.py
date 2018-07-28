from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from users.models import User
from users.serializers import UserSerializer


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_authorization_enforced(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse('user-detail',
                                           kwargs={'pk': self.user.id}))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_list_of_users(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse('user-list'))
        self.assertTrue((status.is_success(response.status_code)))

    def test_create_user(self):
        self.client.force_authenticate(None)
        data = {'username': 'Another Cool Guy',
                'email': 'another_cool_guy@smedialink.com',
                'password': 'qwe'
                }
        response = self.client.post(
            reverse('user-list'),
            data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

    def test_get_user(self):
        response = self.client.get(
            reverse('user-detail',
                    kwargs={'pk': self.user.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, UserSerializer().to_representation(self.user))

    def test_update_user(self):
        user = User.objects.get()
        new_data = {'email': 'not_so_cool_guy@smedialink.com'}
        response = self.client.patch(
            reverse('user-detail', kwargs={'pk': user.id}),
            new_data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

    def test_delete_user(self):
        response = self.client.delete(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            format='json',
            follow=True
        )

        self.assertTrue(status.is_success(response.status_code))
