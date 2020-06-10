import os

from detecto.core import Model, Dataset, DataLoader
from django.core.management import BaseCommand
from django.db import transaction

from vegetable.models import Vegetable, PYTORCH_BASE_DIR


class Command(BaseCommand):
    help = 'Train task for Detecto simple model training.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slug',
            type=str,
            action='store',
            dest='slug',
            default=None,
            help='Vegetable slug.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        slug = options.get('slug')
        try:
            vegetable = Vegetable.objects.get(slug=slug)
        except Vegetable.DoesNotExist:
            self.stdout.write('Vegetable does not exists.')
            return
        model = Model([vegetable.slug, ])
        path = os.path.join(PYTORCH_BASE_DIR, 'images', vegetable.slug)

        dataset = Dataset(path, )
        loader = DataLoader(dataset, batch_size=1)
        model.fit(loader, verbose=True, )
