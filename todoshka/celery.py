import os
from datetime import timedelta

from celery import Celery

from todoshka import settings

# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoshka.settings')
app = Celery('todoshka')

# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-notifications': {
        'task': 'todolists.tasks.notify',
        'schedule': timedelta(minutes=1),
    },
}
app.conf.timezone = 'UTC'
