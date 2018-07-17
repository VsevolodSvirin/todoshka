from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w\.@+\- ]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_, and space characters.'
    )


class User(AbstractUser):
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

    email = models.EmailField(_('email address'), null=False, blank=False)


@receiver(pre_save, sender=User)
def validate_model(sender, instance, **kwargs):
    instance.full_clean()
