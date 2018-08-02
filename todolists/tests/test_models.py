from django.contrib.auth import get_user_model
from django.test import TestCase

from todolists.models import TodoList

User = get_user_model()


class TodoListTestCase(TestCase):
    def test_create_todo_list_success(self):
        user = User.objects.create_user(username='Cool Guy',
                                        email='cool_guy@smedialink.com',
                                        password='123')
        old_count = TodoList.objects.count()

        todolist = TodoList(name='My First ToDo List',
                            author=user)
        todolist.save()
        new_count = TodoList.objects.count()

        self.assertEqual(old_count + 1, new_count)

        user.delete()
        todolist.delete()
