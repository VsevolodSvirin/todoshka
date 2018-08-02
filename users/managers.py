from django.contrib.auth.models import UserManager as DefaultUserManager

from categories.models import Category


class UserManager(DefaultUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = super()._create_user(username, email, password, **extra_fields)

        for category in Category.objects.filter(common=True):
            user.categories.add(category)

        return user
