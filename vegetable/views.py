from rest_framework import viewsets

from vegetable.models import Vegetable
from vegetable.serializers import VegetableSerializer


class VegetableListViewSet(viewsets.ModelViewSet):
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer

    def create(self, request, *args, **kwargs):
        response = super(VegetableListViewSet, self).create(request, *args, **kwargs)
        print(response)
        return response
