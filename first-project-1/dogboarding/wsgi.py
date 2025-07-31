"""
WSGI config for dogboarding project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the Django settings module
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_NAME'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')

print("🚀 Dog Boarding System starting...")
print("✅ Health check: /health/")
print("✅ Emergency fix: /emergency-fix/")

application = get_wsgi_application()
