"""
WSGI config for hidralpress_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from .watchers import batch_watch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hidralpress_backend.settings')

application = get_wsgi_application()
print("Starting to watch for config file changes.")

batch_watch()