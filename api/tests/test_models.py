from django.test import TestCase

from api.models import TodoList
from users.models import User


class TodoListTestCase(TestCase):

    # TODO research if more tests needed
    def test_create_todo_list(self):
        user = User.objects.create(username='Cool Guy')
        old_count = TodoList.objects.count()

        todolist = TodoList(name='My First ToDo List', author=user)
        todolist.save()
        new_count = TodoList.objects.count()

        self.assertEqual(old_count + 1, new_count)
