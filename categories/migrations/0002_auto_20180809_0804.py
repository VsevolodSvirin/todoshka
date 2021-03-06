# Generated by Django 2.0.6 on 2018-08-09 08:04

from django.db import migrations


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.create(name='Home', common=True)
    Category.objects.create(name='Work', common=True)
    Category.objects.create(name='Other', common=True)


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]
