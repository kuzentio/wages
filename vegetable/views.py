import copy

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from vegetable import utils
from vegetable.models import Vegetable, VegetableImage
from vegetable.serializers import VegetableSerializer


class VegetableListViewSet(viewsets.ModelViewSet):
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer


class VegetableImageList(viewsets.ModelViewSet):
    queryset = VegetableImage.objects.all()

    def create(self, request, *args, **kwargs):
        vegetable = get_object_or_404(Vegetable, slug=request.data.get('image_name'))
        image = utils.decode_base64_file(request.data.pop('image_data'))
        data = copy.deepcopy(request.data)
        data['pascalVoc'] = utils.boxes_to_pascal(request.data.get('boxes')[0])  # TODO: processing only first
        vegetable_image = VegetableImage(
            vegetable=vegetable,
            image=image,
            data=data
        )
        vegetable_image.save()

        return Response({'status': 'OK'})
