from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Category
from categories.serializers import CategorySerializer

User = get_user_model()


class CategoryViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.client.force_authenticate(user=self.user)
        self.common_category = Category.objects.create(name='This is a Common Category',
                                                       common=True)
        self.personal_category = Category.objects.create(name='This is a Personal Category')
        self.user.categories.add(self.personal_category)

    def tearDown(self):
        self.user.delete()
        self.common_category.delete()
        self.personal_category.delete()

    def test_authorization_enforced(self):
        self.client.force_authenticate(None)

        response = self.client.get(reverse('category-detail',
                                           kwargs={'pk': self.common_category.id}))
        self.assertTrue(status.is_client_error(response.status_code))

        response = self.client.get(reverse('category-detail',
                                           kwargs={'pk': self.personal_category.id}))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_category(self):
        data = {'name': 'My First Category',
                'user': self.user.id}
        response = self.client.post(
            reverse('category-list'),
            data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

        Category.objects.filter(name='My First Category').first().delete()

    def test_get_category(self):
        response = self.client.get(
            reverse('category-detail',
                    kwargs={'pk': self.common_category.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, CategorySerializer().to_representation(self.common_category))

        response = self.client.get(
            reverse('category-detail',
                    kwargs={'pk': self.personal_category.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, CategorySerializer().to_representation(self.personal_category))

        other_user = User.objects.create_user(username='Bad Guy',
                                              email='bad_guy@smedilink.com',
                                              password='321')
        self.client.force_authenticate(other_user)

        response = self.client.get(
            reverse('category-detail',
                    kwargs={'pk': self.common_category.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, CategorySerializer().to_representation(self.common_category))

        response = self.client.get(
            reverse('category-detail',
                    kwargs={'pk': self.personal_category.id}),
            format='json'
        )

        self.assertTrue(status.is_client_error(response.status_code))

        other_user.delete()

    def test_update_category(self):
        new_data = {'name': 'This is a Category'}
        response = self.client.patch(
            reverse('category-detail', kwargs={'pk': self.personal_category.id}),
            new_data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

        response = self.client.patch(
            reverse('category-detail', kwargs={'pk': self.common_category.id}),
            new_data,
            format='json'
        )

        self.assertTrue(status.is_client_error(response.status_code))

    def test_delete_category(self):
        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': self.personal_category.id}),
            format='json',
            follow=True
        )

        self.assertTrue(status.is_success(response.status_code))

        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': self.common_category.id}),
            format='json',
            follow=True
        )

        self.assertTrue(status.is_client_error(response.status_code))
