from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import TodoList
from api.serializers import TodoListSerializer


class TodoListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Cool Guy')
        self.client.force_authenticate(user=self.user)
        TodoList.objects.create(name='This is a List', author=self.user)

    def test_authorization_enforced(self):
        self.client.force_authenticate(None)
        todo = TodoList.objects.get()
        response = self.client.get(reverse('todolist-detail', kwargs={'pk': todo.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_todo_list(self):
        data = {'name': 'My First ToDo List', 'author': self.user.id}
        response = self.client.post(
            reverse('todolist-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_todo_list(self):
        todo = TodoList.objects.get()
        response = self.client.get(
            reverse('todolist-detail', kwargs={'pk': todo.id}),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TodoListSerializer().to_representation(todo))

    def test_update_todo_list(self):
        todo = TodoList.objects.get()
        new_data = {'name': 'Supa List'}
        response = self.client.patch(
            reverse('todolist-detail', kwargs={'pk': todo.id}),
            new_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_todo_list(self):
        todo = TodoList.objects.get()
        response = self.client.delete(
            reverse('todolist-detail', kwargs={'pk': todo.id}),
            format='json',
            follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
