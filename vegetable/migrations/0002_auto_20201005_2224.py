# Generated by Django 3.0.6 on 2020-10-05 22:24

from django.db import migrations
from django_celery_beat.models import DAYS


def create_train_task(apps, schema_editor):
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
    IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')
    every_day = IntervalSchedule.objects.create(
        every=1, period=DAYS
    )
    PeriodicTask.objects.create(
        name='Training',  task='vegetable.tasks.running_training', interval=every_day, enabled=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('vegetable', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_train_task, reverse_code=migrations.RunPython.noop)
    ]
