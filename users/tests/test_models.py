from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def test_create_user_success(self):
        old_count = User.objects.count()

        User.objects.create_user(username='Cool Guy',
                                 email='cool_guy@smedilink.com',
                                 password='123')
        new_count = User.objects.count()

        self.assertEqual(old_count + 1, new_count)

    def test_bad_username_fail(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='(C)ool Gu¥',
                                     email='cool_guy@smedilink.com',
                                     password='123')

    def test_missing_fields_fail(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='Bad Guy',
                                     email='bad_guy@smedilink.com')

            User.objects.create_user(username='Bad Guy',
                                     password='321')

            User.objects.create_user(email='bad_guy@smedilink.com',
                                     password='321')
