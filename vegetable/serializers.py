from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from vegetable.models import Vegetable


class VegetableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vegetable
        fields = ('pk', 'name', 'slug')
        read_only_fields = ('slug', )

    def validate_name(self, attrs):
        if len(attrs) <= 0:
            raise ValidationError("Name can not be empty.")
        if Vegetable.objects.filter(slug=slugify(attrs)).exists():
            raise ValidationError("This product already exists.")
        return attrs
