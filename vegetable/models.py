import os

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.files.images import get_image_dimensions
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.text import slugify

from vegetable.utils import image_and_annotation_folder

PYTORCH_BASE_DIR = os.path.join(settings.BASE_DIR, 'PyTorch')


def pytorch_path(instance, filename):
    return os.path.join(PYTORCH_BASE_DIR, image_and_annotation_folder(), '{slug}-{filename}'.format(
        slug=instance.vegetable.slug, filename=filename
    ))


class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Vegetable, self).save(force_insert, force_update, using, update_fields)


class VegetableImage(models.Model):
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pytorch_path)
    data = JSONField(default=dict)

    def get_context_for_pascal_voc(self):
        path = self.image.file.name

        width, height = get_image_dimensions(self.image.file)
        context = {
            'filename': path.split('/')[-1],
            'path': path,
            'width': width,
            'height': height,
            'name': self.vegetable.slug,
        }
        context.update(self.data['pascalVoc'])

        return context

    def create_annotation_file(self):
        filename = self.image.name
        xml_file = filename.split('.')[0] + '.xml'
        with open(xml_file, 'w') as file:
            file.write(render_to_string('pascal_voc.xml', self.get_context_for_pascal_voc()))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(VegetableImage, self).save(force_insert, force_update, using, update_fields)
        self.create_annotation_file()
