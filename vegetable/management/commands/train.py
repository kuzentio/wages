import os

from detecto.core import Model, Dataset, DataLoader
from django.core.management import BaseCommand
from django.db import transaction

from vegetable.models import Vegetable
from vegetable.tasks import running_training


class Command(BaseCommand):
    help = 'Train task for Detecto simple model training.'
    queryset = Vegetable.objects.all()

    @transaction.atomic
    def handle(self, *args, **options):
        running_training()
