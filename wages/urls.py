from django.conf import settings
from django.contrib import admin
from django.urls import path

from api.urls import vegetable_list
from core.views import index


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/vegetables/', vegetable_list, name='vegetable-list'),

]

if settings.DEBUG:
    urlpatterns += path("", index, name="index"),
