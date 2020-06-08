import os

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.utils.text import slugify


PYTORCH_BASE_DIR = os.path.join(settings.BASE_DIR, 'PyTorch')


def pytorch_path(instance, filename):
    return os.path.join(PYTORCH_BASE_DIR, 'images', instance.vegetable.slug, filename)


class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def get_or_create_pytorch_dir(self):
        pytorch_dir = os.path.join(PYTORCH_BASE_DIR, 'images', self.slug)
        if not os.path.exists(pytorch_dir):
            os.makedirs(pytorch_dir)
        return pytorch_dir

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        self.get_or_create_pytorch_dir()
        super(Vegetable, self).save(force_insert, force_update, using, update_fields)


class VegetableImage(models.Model):
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pytorch_path)
    data = JSONField(default=dict)
