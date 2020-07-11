import os

from detecto.core import Model, Dataset, DataLoader

from celery import shared_task

from vegetable.models import PYTORCH_BASE_DIR, Vegetable
from vegetable.utils import image_and_annotation_folder

models_path = f'{PYTORCH_BASE_DIR}/models/'


@shared_task
def running_training():
    slugs = Vegetable.objects.all().values_list('slug', flat=True)
    model = Model(list(slugs))
    dataset = Dataset(
        os.path.join(PYTORCH_BASE_DIR, image_and_annotation_folder())
    )
    loader = DataLoader(dataset, batch_size=1)
    model.fit(loader, verbose=True)
    if not os.path.exists(models_path):
        os.makedirs(models_path)
    model.save(os.path.join(models_path, 'test.pth'))
