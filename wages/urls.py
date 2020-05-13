from django.conf import settings
from django.contrib import admin
from django.urls import path

from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += path("", index, name="index"),
