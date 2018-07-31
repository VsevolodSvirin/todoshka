from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category
from categories.serializers import CategorySerializer

User = get_user_model()


class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.category_attrs = {
            'name': 'My Category',
            'user': self.user
        }

        self.category_obj = Category.objects.create(**self.category_attrs)
        self.category_serialized = CategorySerializer(instance=self.category_obj)

    def tearDown(self):
        self.user.delete()
        self.category_obj.delete()

    def test_contains_expected_fields(self):
        data = self.category_serialized.data

        self.assertEqual(set(data.keys()), {'id', 'name', 'common', 'user'})

    def test_fields_content(self):
        data = self.category_serialized.data

        self.assertEqual(data['name'], self.category_attrs['name'])
        self.assertEqual(data['common'], Category._meta.get_field('common').default)
        self.assertEqual(data['user'], self.category_attrs['user'].id)
