from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def test_create_user(self):
        old_count = User.objects.count()

        User.objects.create_user(username='Cool Guy',
                                 email='cool_guy@smedilink.com',
                                 password='123')
        new_count = User.objects.count()

        self.assertEqual(old_count + 1, new_count)

    def test_no_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='Not So Cool Guy',
                                     password='123')
