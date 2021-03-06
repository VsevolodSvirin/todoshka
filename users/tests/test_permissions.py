from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from users.models import User
from users.permissions import IsSelfOrAdmin
from users.views import UserViewSet


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.view = UserViewSet()

        self.permission = IsSelfOrAdmin()

        self.user = User.objects.create_user(username='Awesome Bob',
                                             email='awesome@bob.com',
                                             password='123')
        self.user_2 = User.objects.create_user(username='Magnificent Jane',
                                               email='magnificent@jane.com',
                                               password='123')
        self.admin = User.objects.create_superuser(username='Reckless Joe',
                                                   email='reckless@joe.com',
                                                   password='12345678')

    def tearDown(self):
        self.user.delete()
        self.user_2.delete()
        self.admin.delete()

    def test_admin_can_edit_everybody(self):
        self.mock_request.user = self.admin
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user)

        self.assertTrue(response)

    def test_user_can_edit_himself(self):
        self.mock_request.user = self.user
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user)

        self.assertTrue(response)

    def test_user_cannot_edit_others(self):
        self.mock_request.user = self.user_2
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user)

        self.assertFalse(response)

    def test_cannot_do_anything_without_authentication(self):
        self.mock_request.user = AnonymousUser()
        response = self.permission.has_permission(self.mock_request, self.view)

        self.assertFalse(response)
