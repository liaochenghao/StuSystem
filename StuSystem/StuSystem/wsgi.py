"""
WSGI config for StuSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from StuSystem.auto import start_auto_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StuSystem.settings")

application = get_wsgi_application()
start_auto_task()
