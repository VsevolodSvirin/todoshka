from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todolists.models import TodoList
from todolists.serializers import TodoListSerializer

User = get_user_model()


class TodoListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.client.force_authenticate(user=self.user)
        self.todolist = TodoList.objects.create(name='This is a List',
                                                author=self.user)

    def tearDown(self):
        self.user.delete()
        self.todolist.delete()

    def test_authorization_enforced(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse('todolist-detail',
                                           kwargs={'pk': self.todolist.id}))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_todo_list(self):
        data = {'name': 'My First ToDo List',
                'author': self.user.id}
        response = self.client.post(
            reverse('todolist-list'),
            data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

        TodoList.objects.filter(name='My First ToDo List').first().delete()

    def test_get_todo_list(self):
        response = self.client.get(
            reverse('todolist-detail',
                    kwargs={'pk': self.todolist.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, TodoListSerializer().to_representation(self.todolist))

    def test_update_todo_list(self):
        new_data = {'name': 'Supa List'}
        response = self.client.patch(
            reverse('todolist-detail', kwargs={'pk': self.todolist.id}),
            new_data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

    def test_delete_todo_list(self):
        response = self.client.delete(
            reverse('todolist-detail', kwargs={'pk': self.todolist.id}),
            format='json',
            follow=True
        )

        self.assertTrue(status.is_success(response.status_code))
