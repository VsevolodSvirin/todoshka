from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.serializers import TaskSerializer

User = get_user_model()


class EmailServicesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Cool Guy',
                                        email='cool_guy@smedialink.com',
                                        password='123')
        self.assignee = User.objects.create(username='Another Cool Guy',
                                            email='another_cool_guy@smedialink.com',
                                            password='123')

    @patch('todolists.services.email_task_assigned.delay')
    def test_email_delivery_service_on_create(self, task_assigned_delay):
        todo_attrs = {
            'name': 'My ToDo List',
            'author': self.user,
            'assignee': self.assignee
        }
        instance = TaskSerializer().create(validated_data=todo_attrs)

        task_assigned_delay.called_with(instance, todo_attrs)

    @patch('todolists.services.email_task_assigned.delay')
    @patch('todolists.services.email_deadline_changed.delay')
    def test_email_delivery_service_on_update(self, deadline_changed_delay, task_assigned_delay):
        todo_attrs = {
            'name': 'My ToDo List',
            'author': self.user,
            'assignee': self.assignee
        }
        instance = TaskSerializer().create(validated_data=todo_attrs)

        new_assignee = User.objects.create(username='Awesome Bob',
                                           email='awesome@bob.com',
                                           password='123')
        instance = TaskSerializer().update(instance, validated_data={'assignee': new_assignee})

        task_assigned_delay.called_with(instance, {'assignee': new_assignee})

        time = {'deadline': timezone.now() + timedelta(hours=1)}
        instance = TaskSerializer().update(instance, time)

        deadline_changed_delay.called_with(instance, {'deadline': time})
