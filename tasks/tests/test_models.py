from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.models import Task

User = get_user_model()


class TaskTestCase(TestCase):
    def test_create_todo_list_success(self):
        user = User.objects.create_user(username='Cool Guy',
                                        email='cool_guy@smedialink.com',
                                        password='123')
        old_count = Task.objects.count()

        task = Task(name='My First ToDo List',
                    author=user)
        task.save()
        new_count = Task.objects.count()

        self.assertEqual(old_count + 1, new_count)

        user.delete()
        task.delete()
