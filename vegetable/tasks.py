import os

from detecto.core import Model, Dataset, DataLoader

from celery import shared_task

from vegetable.models import PYTORCH_BASE_DIR, Vegetable


@shared_task
def running_training():
    slugs = list(Vegetable.objects.all().values_list('slug', flat=True))
    model = Model(slugs)
    dataset_path = os.path.join(PYTORCH_BASE_DIR, 'images')
    dataset = Dataset(dataset_path)
    loader = DataLoader(
        dataset, batch_size=1
    )
    model.fit(loader, verbose=True)

    model.save('{path}/models/test.pth'.format(path=PYTORCH_BASE_DIR))
