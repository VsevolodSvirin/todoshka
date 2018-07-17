from django.test import TestCase

from users.models import User
from users.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_attrs = {
            'username': 'Cool Guy'
        }

        self.user_obj = User.objects.create(**self.user_attrs)
        self.user_serialized = UserSerializer(instance=self.user_obj)

    def test_contains_expected_fields(self):
        data = self.user_serialized.data

        self.assertCountEqual(data.keys(), {'username'})

    def test_fields_content(self):
        data = self.user_serialized.data

        self.assertEqual(data['username'], self.user_attrs['username'])
