# Generated by Django 2.0.6 on 2018-08-02 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todolists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_todolists', to=settings.AUTH_USER_MODEL),
        ),
    ]
