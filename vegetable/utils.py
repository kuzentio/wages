import os

from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr

from django.core.files.images import get_image_dimensions


def decode_base64_file(data):
    def get_file_extension(file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        return ContentFile(decoded_file, name=complete_file_name)


def boxes_to_pascal(boxes=None, image=None):
    if boxes is None:
        return
    pascal_voc = {
        'xmin': round(boxes['x']),
        'ymin': round(boxes['y']),
        'xmax': round(boxes['w'] + boxes['x']),
        'ymax': round(boxes['h'] + boxes['y'])
    }

    return pascal_voc


def image_and_annotation_folder():
    folder = 'images'
    if not os.getenv('ENV') == 'nano':
        folder = 'test-' + folder
    return folder
