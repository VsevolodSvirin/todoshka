from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey('users.User', related_name='tasks', on_delete=models.CASCADE)
    assignee = models.ForeignKey('users.User', related_name='assigned_tasks', null=True, blank=True,
                                 on_delete=models.SET_NULL,)
    category = models.ForeignKey('categories.Category', related_name='tasks', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    deadline = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to="media/tasks/images/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
