from django.db import models


class RecogniseRequest(models.Model):
    image = models.ImageField(upload_to='recognition')
    created_at = models.DateTimeField(auto_now=True, editable=False)
