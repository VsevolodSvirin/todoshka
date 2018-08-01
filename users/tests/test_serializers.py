from django.test import TestCase

from users.models import User
from users.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_attrs = {
            'username': 'Cool Guy',
            'email': 'cool_guy@smedialink.com',
        }

        self.user_obj = User.objects.create_user(**self.user_attrs)
        self.user_serialized = UserSerializer(instance=self.user_obj)

    def tearDown(self):
        self.user_obj.delete()

    def test_contains_expected_fields(self):
        data = self.user_serialized.data

        self.assertEqual(set(data.keys()), {'id', 'username', 'email'})

    def test_fields_content(self):
        data = self.user_serialized.data

        self.assertEqual(data['username'], self.user_attrs['username'])
        self.assertEqual(data['email'], self.user_attrs['email'])

    def test_create_user_is_not_possible(self):
        user_attrs = {
            'username': 'Another Cool Guy',
            'email': 'another_cool_guy@smedialink.com',
        }
        with self.assertRaises(NotImplementedError):
            UserSerializer().create(validated_data=user_attrs)
