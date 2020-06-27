import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.local')

app = Celery('wages')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
