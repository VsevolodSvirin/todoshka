from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def test_create_user(self):
        old_count = User.objects.count()

        user = User.objects.create(username='Cool Guy')
        user.save()
        new_count = User.objects.count()

        self.assertEqual(old_count + 1, new_count)
