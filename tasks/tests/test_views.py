from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task
from tasks.serializers import TaskSerializer

User = get_user_model()


class TaskViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(name='This is a List',
                                        author=self.user)

    def tearDown(self):
        self.user.delete()
        self.task.delete()

    def test_authorization_enforced(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse('task-detail',
                                           kwargs={'pk': self.task.id}))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_todo_list(self):
        data = {'name': 'My First ToDo List',
                'author': self.user.id}
        response = self.client.post(
            reverse('task-list'),
            data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

        Task.objects.filter(name='My First ToDo List').first().delete()

    def test_get_todo_list(self):
        response = self.client.get(
            reverse('task-detail',
                    kwargs={'pk': self.task.id}),
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, TaskSerializer().to_representation(self.task))

    def test_update_todo_list(self):
        new_data = {'name': 'Supa List'}
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task.id}),
            new_data,
            format='json'
        )

        self.assertTrue(status.is_success(response.status_code))

    def test_delete_todo_list(self):
        response = self.client.delete(
            reverse('task-detail', kwargs={'pk': self.task.id}),
            format='json',
            follow=True
        )

        self.assertTrue(status.is_success(response.status_code))
