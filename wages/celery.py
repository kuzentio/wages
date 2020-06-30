import os

import django
from celery import Celery

if os.environ.get('ENV') is not None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.{}'.format(os.environ.get('ENV')))
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.local')

django.setup()
app = Celery('wages')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
