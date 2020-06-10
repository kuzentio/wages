import os

from detecto.core import Model, Dataset, DataLoader

from celery import shared_task

from vegetable.models import PYTORCH_BASE_DIR


@shared_task
def running_training():
    slug = 'face-one'
    model = Model([slug, ])
    path = os.path.join(PYTORCH_BASE_DIR, 'images', slug)

    dataset = Dataset(path, )
    loader = DataLoader(dataset, batch_size=1)
    model.fit(loader, verbose=True, )
