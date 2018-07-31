from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category

User = get_user_model()


class CategoriesTestCase(TestCase):
    def test_create_todo_list_success(self):
        user = User.objects.create_user(username='Cool Guy',
                                        email='cool_guy@smedilink.com',
                                        password='123')
        old_count = Category.objects.count()

        category_1 = Category(name='My First Category')
        category_1.save()
        new_count = Category.objects.count()

        self.assertEqual(old_count + 1, new_count)

        category_2 = Category(name='My Second Category',
                              user=user)
        category_2.save()

        old_count = new_count
        new_count = Category.objects.count()

        self.assertEqual(old_count + 1, new_count)

        category_3 = Category(name='My Third Category',
                              common=True)
        category_3.save()

        old_count = new_count
        new_count = Category.objects.count()

        self.assertEqual(old_count + 1, new_count)

        user.delete()
        category_1.delete()
        category_2.delete()
        category_3.delete()
