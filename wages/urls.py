from django.conf import settings
from django.contrib import admin
from django.urls import path

from core.views import index, capture_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/foobar/', capture_image),
]

if settings.DEBUG:
    urlpatterns += path("", index, name="index"),
