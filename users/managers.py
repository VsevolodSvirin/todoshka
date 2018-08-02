from django.contrib.auth.models import UserManager as DefaultUserManager

from categories.models import Category


class UserManager(DefaultUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = super()._create_user(username, email, password, **extra_fields)

        for category in Category.objects.filter(common=True):
            user.categories.add(category)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
