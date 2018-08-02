from django.test import TestCase

from categories.models import Category
from categories.serializers import CategorySerializer


class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.category_attrs = {
            'name': 'My Category',
        }

        self.category_obj = Category.objects.create(**self.category_attrs)
        self.category_serialized = CategorySerializer(instance=self.category_obj)

    def tearDown(self):
        self.category_obj.delete()

    def test_contains_expected_fields(self):
        data = self.category_serialized.data

        self.assertEqual(set(data.keys()), {'id', 'name', 'common'})

    def test_fields_content(self):
        data = self.category_serialized.data

        self.assertEqual(data['name'], self.category_attrs['name'])
        self.assertEqual(data['common'], Category._meta.get_field('common').default)
