from django.db import models


class TodoList(models.Model):
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey('users.User', related_name='todolists', on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', related_name='todolists', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
