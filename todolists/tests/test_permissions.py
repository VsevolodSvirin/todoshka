from unittest.mock import Mock

from django.test import TestCase

from todolists.models import TodoList
from todolists.permissions import IsAuthorOrAdmin
from users.models import User


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.permission = IsAuthorOrAdmin()

        self.user = User.objects.create_user(username='Awesome Bob',
                                             email='awesome@bob.com',
                                             password='123')
        self.user_2 = User.objects.create_user(username='Magnificent Jane',
                                               email='magnificent@jane.com',
                                               password='123')
        self.admin = User.objects.create_superuser(username='Reckless Joe',
                                                   email='lul@olo.lo',
                                                   password='12345678')

        self.user_todo_list = TodoList.objects.create(name='Bobby\'s List',
                                                      author=self.user)

    def test_admin_can_edit_everything(self):
        self.mock_request.user = self.admin
        response = self.permission.has_object_permission(self.mock_request, None, self.user_todo_list)

        self.assertTrue(response)

    def test_user_can_edit_his_list(self):
        self.mock_request.user = self.user
        response = self.permission.has_object_permission(self.mock_request, None, self.user_todo_list)

        self.assertTrue(response)

    def test_user_cannot_edit_list_of_another_user(self):
        self.mock_request.user = self.user_2
        response = self.permission.has_object_permission(self.mock_request, None, self.user_todo_list)

        self.assertFalse(response)
