from django.conf import settings
from django.contrib import admin
from django.urls import path

from api.urls import vegetable_list, vegetable_image_list
from core.views import index
from recognition.urls import recognise_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/vegetables/', vegetable_list, name='vegetable-list'),
    path('api/vegetable/images/', vegetable_image_list, name='vegetable-image-list'),
    path('api/recognize/', recognise_view, name='recognize'),
]

if settings.DEBUG:
    urlpatterns += path("", index, name="index"),
