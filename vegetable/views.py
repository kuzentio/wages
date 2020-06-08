from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from vegetable.models import Vegetable, VegetableImage
from vegetable.serializers import VegetableSerializer
from vegetable.utils import decode_base64_file


class VegetableListViewSet(viewsets.ModelViewSet):
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer


class VegetableImageList(viewsets.ModelViewSet):
    queryset = VegetableImage.objects.all()

    def create(self, request, *args, **kwargs):
        vegetable = get_object_or_404(Vegetable, slug=request.data.get('image_name'))
        vegetable_image = VegetableImage(
            vegetable=vegetable,
            image=decode_base64_file(request.data.pop('image_data')),
            data=request.data
        )
        vegetable_image.save()

        return Response({'status': 'OK'})
