from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    common = models.BooleanField(default=False)
