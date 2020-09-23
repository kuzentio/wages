import os

import torch
from celery import shared_task

from vegetable.models import PYTORCH_BASE_DIR, Vegetable
from vegetable.utils import image_and_annotation_folder

models_path = f'{PYTORCH_BASE_DIR}/models/'


@shared_task
def running_training():
    from detecto.core import Model, Dataset, DataLoader

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    slugs = Vegetable.objects.all().values_list('slug', flat=True)
    dataset = Dataset(
        os.path.join(PYTORCH_BASE_DIR, image_and_annotation_folder())
    )
    loader = DataLoader(dataset, batch_size=1)
    model = Model(list(slugs), device=device)
    model.fit(loader, verbose=True)
    if not os.path.exists(models_path):
        os.makedirs(models_path)
    model.save(os.path.join(models_path, 'test.pth'))
