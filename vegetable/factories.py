from datetime import datetime

from django.contrib.auth import models as auth_models
from factory import DjangoModelFactory, LazyFunction, SubFactory, Sequence
from factory.django import ImageField

from vegetable import models
from vegetable.models import VegetableImage


class UserFactory(DjangoModelFactory):
    class Meta:
        model = auth_models.User

    first_name = 'John'
    last_name = 'Doe'
    email = 'john-doe@example.com'
    date_joined = LazyFunction(datetime.now)


class VegetableFactory(DjangoModelFactory):
    class Meta:
        model = models.Vegetable
    name = Sequence(lambda n: 'apple-{}'.format(n))


class VegetableImageFactory(DjangoModelFactory):
    class Meta:
        model = VegetableImage

    vegetable = SubFactory(VegetableFactory)
    image = ImageField()
    data = {'pascalVoc': ''}
