from django.contrib.auth import get_user_model
from django.test import TestCase

from todolists.models import TodoList
from todolists.serializers import TodoListSerializer


User = get_user_model()


class TodoListSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.todo_attrs = {
            'name': 'My ToDo List',
            'author': self.user
        }

        self.todo_obj = TodoList.objects.create(**self.todo_attrs)
        self.todo_serialized = TodoListSerializer(instance=self.todo_obj)

    def tearDown(self):
        self.user.delete()
        self.todo_obj.delete()

    def test_contains_expected_fields(self):
        data = self.todo_serialized.data

        self.assertEqual(set(data.keys()), {'id', 'name', 'author', 'date_created', 'date_modified'})

    def test_fields_content(self):
        data = self.todo_serialized.data

        self.assertEqual(data['name'], self.todo_attrs['name'])
        self.assertEqual(data['author'], self.todo_attrs['author'].id)

    def test_dates(self):
        data = self.todo_serialized.data

        self.assertLess(data['date_created'], data['date_modified'])
