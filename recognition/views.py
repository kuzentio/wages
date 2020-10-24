import json
import os
from PIL import Image
from detecto import core, utils
from rest_framework import viewsets
from rest_framework.response import Response

from vegetable import utils
from vegetable.models import PYTORCH_BASE_DIR, Vegetable

PATH = os.path.join(PYTORCH_BASE_DIR, 'models', 'test.pth')


# def recognize(request):
#     model = core.Model.load(
#         PATH,
#         list(Vegetable.objects.all().order_by('id').values_list('slug', flat=True))
#     )
#     image_data = json.loads(request.body).get('image_data')
#     img_file = utils.decode_base64_file(image_data)
#     img = Image.open(img_file)
#     labels, boxes, scores = model.predict_top(img)
#     predictions = zip(labels, [s.item() for s in scores])
#     return JsonResponse({
#         'success': True,
#         'predictions': list(predictions),
#     })


class RecogniseViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        model = core.Model.load(
            PATH,
            list(Vegetable.objects.all().order_by('id').values_list('slug', flat=True))
        )
        image_data = json.loads(request.body).get('image_data')
        img_file = utils.decode_base64_file(image_data)
        img = Image.open(img_file)
        labels, boxes, scores = model.predict_top(img)
        predictions = zip(labels, [s.item() for s in scores])
        return Response({
            'success': True,
            'predictions': list(predictions),
        })
