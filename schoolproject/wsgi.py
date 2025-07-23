import os

from django.core.wsgi import get_wsgi_application

settings_module = 'schoolproject.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'schoolproject.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

application = get_wsgi_application()
