import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.exceptions import ValidationError

from tasks.models import Task
from tasks.serializers import TaskSerializer

User = get_user_model()


class TaskSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.assignee = User.objects.create_user(username='Another Cool Guy',
                                                 email='another_cool_guy@smedialink.com',
                                                 password='123')
        self.todo_attrs = {
            'name': 'My ToDo List',
            'author': self.user,
            'assignee': self.assignee,
            'deadline': datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=UTC)
        }

        self.todo_obj = Task.objects.create(**self.todo_attrs)
        self.todo_serialized = TaskSerializer(instance=self.todo_obj)

    def tearDown(self):
        self.user.delete()
        self.assignee.delete()
        self.todo_obj.delete()

    def test_contains_expected_fields(self):
        data = self.todo_serialized.data

        self.assertEqual(set(data.keys()), {'id', 'name', 'author', 'assignee', 'category', 'deadline',
                                            'date_created', 'date_modified'})

    def test_fields_content(self):
        data = self.todo_serialized.data

        self.assertEqual(data['name'], self.todo_attrs['name'])
        self.assertEqual(data['author'], self.todo_attrs['author'].id)
        self.assertEqual(data['assignee'], self.todo_attrs['assignee'].id)
        self.assertEqual(data['category'], None)

    def test_dates(self):
        data = self.todo_serialized.data

        self.assertLess(data['date_created'], data['deadline'])
        self.assertLess(data['date_created'], data['date_modified'])

    def test_deadline_after_now_fail(self):
        todo_attrs = {
            'name': 'My Second ToDo List',
            'author': self.user.id,
            'assignee': self.assignee.id,
            'deadline': timezone.now() - datetime.timedelta(hours=1)
        }
        with self.assertRaises(ValidationError):
            TaskSerializer(data=todo_attrs).is_valid(raise_exception=True)

    @patch('tasks.serializers.deliver_email_on_create')
    @patch('tasks.serializers.deliver_email_on_update')
    def test_email_delivery(self, deliver_email_on_update, deliver_email_on_create):
        todo_attrs = {
            'name': 'My Second ToDo List',
            'author': self.user,
            'assignee': self.assignee,
            'deadline': datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=UTC)
        }

        todo_obj = TaskSerializer().create(todo_attrs)
        deliver_email_on_create.assert_called()

        TaskSerializer().update(todo_obj,
                                {'deadline': datetime.datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)})
        deliver_email_on_update.assert_called()
