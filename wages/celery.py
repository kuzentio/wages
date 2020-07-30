import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"wages.settings.{os.getenv('ENV', default='local')}")

app = Celery('wages')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
