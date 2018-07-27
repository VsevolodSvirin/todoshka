from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def test_create_user_success(self):
        old_count = User.objects.count()

        user = User.objects.create_user(username='Cool Guy',
                                        email='cool_guy@smedilink.com',
                                        password='123')
        new_count = User.objects.count()

        self.assertEqual(old_count + 1, new_count)

        user.delete()

    def test_bad_username_fail(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='(C)ool Gu¥',
                                     email='cool_guy@smedilink.com',
                                     password='123')

    def test_missing_fields_fail(self):
        # If password is None then return a concatenation of UNUSABLE_PASSWORD_PREFIX and
        # a random string, which disallows logins. See django.contrib.auth.hashers.make_password.
        user = User.objects.create_user(username='Bad Guy',
                                        email='bad_guy@smedilink.com')
        self.assertTrue(user.password.startswith('!'))

        with self.assertRaises(ValidationError):
            User.objects.create_user(username='Bad Guy',
                                     password='321')

        # Username is a required positional argument.
        with self.assertRaises(TypeError):
            User.objects.create_user(email='bad_guy@smedilink.com',
                                     password='321')
