import json
import os
from PIL import Image
from detecto import core, utils
from django.http import JsonResponse

from vegetable import utils
from vegetable.models import PYTORCH_BASE_DIR, Vegetable

PATH = os.path.join(PYTORCH_BASE_DIR, 'models', 'test.pth')


def recognize(request):
    model = core.Model.load(
        PATH,
        list(Vegetable.objects.all().order_by('id').values_list('slug', flat=True))
    )
    image_data = json.loads(request.body).get('image_data')
    img_file = utils.decode_base64_file(image_data)
    img = Image.open(img_file)
    labels, boxes, scores = model.predict_top(img)
    predictions = zip(labels, [s.item() for s in scores])
    return JsonResponse({
        'success': True,
        'predictions': list(predictions),
    })





#
#
#
# Hi Kristian,
# I'm Igor. We  had worked together I hope you remember me =)))
# I'm good, i got success in software development, now i have been working in big american medecine company at seniour position.
# My success would not have been possible without experience which I got at the Unisport.
# I should say many thanks to you for your patience and attention to details.
#
# I'm writing with a referance to the vacancy https://www.unisportstore.com/blog/11894-backend-engineer-read-more-about-the-job-at-unisport/
# And I would like to recommend you my brother.
# He has experience of building projects from scratch and maintaing launched sites from freelance.
# Now he is looking for company where he can boost his skills, and I guess he reached the level of working at this position.

#
#
# His CV in attachments.
#
# Thank you for given time and attention.
#
#
#
#
#
# # TODO: (!)
# Summary:
# Backend developer with Python/Django background, and also willing interest in React.
# I'm looking compony where my outstanding skills will have a positive contribution to the Company and increase its success.
# I'm looking for an opportunity where I can show my high-quality work in order to achieve better results for the Company.
#
#
# Experience:
# Links to CTO, ,
#     EasyPay
#     https://alterair.ua/
