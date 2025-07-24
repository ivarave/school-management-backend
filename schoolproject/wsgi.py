import os
from django.core.wsgi import get_wsgi_application

settings_module = 'schoolproject.deployment_settings' if os.environ.get('DJANGO_SETTINGS_MODULE') == 'schoolproject.deployment_settings' else 'schoolproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
