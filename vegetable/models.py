from django.db import models
from django.utils.text import slugify


class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Vegetable, self).save(force_insert, force_update, using,update_fields)
