from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from todolists.models import TodoList
from todolists.permissions import TodoListsPermissions
from todolists.views import TodoListViewSet

User = get_user_model()


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.view = TodoListViewSet()

        self.permission = TodoListsPermissions()

        self.user = User.objects.create_user(username='Awesome Bob',
                                             email='awesome@bob.com',
                                             password='123')
        self.user_2 = User.objects.create_user(username='Magnificent Jane',
                                               email='magnificent@jane.com',
                                               password='123')
        self.admin = User.objects.create_superuser(username='Reckless Joe',
                                                   email='reckless@joe.com',
                                                   password='12345678')

        self.user_todo_list = TodoList.objects.create(name='Bobby\'s List',
                                                      author=self.user)

    def tearDown(self):
        self.user.delete()
        self.user_2.delete()
        self.admin.delete()
        self.user_todo_list.delete()

    def test_admin_can_edit_everything(self):
        self.mock_request.user = self.admin
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_todo_list)

        self.assertTrue(response)

    def test_user_can_edit_his_list(self):
        self.mock_request.user = self.user
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_todo_list)

        self.assertTrue(response)

    def test_user_cannot_edit_list_of_another_user(self):
        self.mock_request.user = self.user_2
        response = self.permission.has_object_permission(self.mock_request, self.view, self.user_todo_list)

        self.assertFalse(response)

    def test_user_can_get_assigned_list(self):
        self.mock_request.user = self.user_2
        self.mock_request.method = 'GET'
        self.user_todo_list.assignee = self.user_2
        response = self.permission.has_object_permission(self.mock_request, None, self.user_todo_list)

        self.assertTrue(response)

    def test_user_can_not_edit_assigned_list(self):
        self.mock_request.user = self.user_2
        self.mock_request.method = 'PATCH'
        response = self.permission.has_object_permission(self.mock_request, None, self.user_todo_list)

        self.assertFalse(response)
