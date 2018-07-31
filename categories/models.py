from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=False)
    common = models.BooleanField(default=False)
    user = models.ForeignKey('users.User', related_name='categories', null=True, blank=True,
                             on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
