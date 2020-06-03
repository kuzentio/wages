from rest_framework import serializers

from vegetable.models import Vegetable


class VegetableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vegetable
        fields = ('pk', 'name', 'slug')
        read_only_fields = ('slug', )

