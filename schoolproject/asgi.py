import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()


settings_module = 'schoolproject.deployment_settings' if os.getenv("DJANGO_ENV") == "production" else 'schoolproject.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module


application = get_asgi_application()
