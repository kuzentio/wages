"""
WSGI config for wages project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('ENV') is not None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.{}'.format(os.environ.get('ENV')))
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wages.settings.local')

application = get_wsgi_application()
