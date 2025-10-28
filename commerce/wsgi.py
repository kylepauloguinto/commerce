"""
WSGI config for commerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

application = get_wsgi_application()

# Wrap it with WhiteNoise
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), 'staticfiles'), max_age=31536000)