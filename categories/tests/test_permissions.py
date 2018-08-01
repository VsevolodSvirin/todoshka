from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category
from categories.permissions import CategoryPermissions
from categories.views import CategoryViewSet

User = get_user_model()


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.view = CategoryViewSet(action='update')

        self.permission = CategoryPermissions()

        self.user = User.objects.create_user(username='Awesome Bob',
                                             email='awesome@bob.com',
                                             password='123')
        self.user_2 = User.objects.create_user(username='Magnificent Jane',
                                               email='magnificent@jane.com',
                                               password='123')
        self.admin = User.objects.create_superuser(username='Reckless Joe',
                                                   email='reckless@joe.com',
                                                   password='12345678')

        self.user_category = Category.objects.create(name='Bobby\'s Category',
                                                     user=self.user)

    def tearDown(self):
        self.user.delete()
        self.user_2.delete()
        self.admin.delete()
        self.user_category.delete()

    def test_admin_can_edit_everything(self):
        self.mock_request.user = self.admin
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_category)

        self.assertTrue(response)

    def test_user_can_edit_his_category(self):
        self.mock_request.user = self.user
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_category)

        self.assertTrue(response)

    def test_user_cannot_edit_category_of_another_user(self):
        self.mock_request.user = self.user_2
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_category)

        self.assertFalse(response)
