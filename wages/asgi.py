"""
ASGI config for wages project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.environ.get('ENV') is not None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.{}'.format(os.environ.get('ENV')))
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.local')

application = get_asgi_application()
