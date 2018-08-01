import base64
import os
import time

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from users.managers import UserManager


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w\.@+\- ]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_, and space characters.'
    )


class User(AbstractUser):
    objects = UserManager()
    username_validator = UsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits, spaces and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), null=False, blank=False, unique=True)

    categories = models.ManyToManyField(Category)

    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token_issued_at = models.IntegerField(default=0)

    def get_refresh_token(self):
        if self.refresh_token is None:
            self.update_refresh_token()
        return self.refresh_token

    def update_refresh_token(self):
        self.refresh_token = get_random_token()
        self.refresh_token_issued_at = time.time()
        self.save(update_fields=['refresh_token_issued_at', 'refresh_token'])


def get_random_token(length=128):
    return base64.b64encode(os.urandom(length)).decode()


@receiver(pre_save, sender=User)
def validate_model(sender, instance, **kwargs):
    instance.full_clean()
