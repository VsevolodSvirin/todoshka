from django.test import TestCase

from users.models import User


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.manager = User.objects

    def tearDown(self):
        self.manager.all().delete()

    def test_default_categories_added(self):
        obj = self.manager.create_user(username='Cool Guy',
                                       email='cool_guy@smedialink.com',
                                       password='123')
        categories = []
        for category in list(obj.categories.all()):
            categories.append(category.name)
        self.assertEqual(categories, ['Home', 'Work', 'Other'])
