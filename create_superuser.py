import os
import django

# Only run if the flag is set to True
if os.environ.get('CREATE_SUPERUSER', 'False') != 'True':
    print("Superuser creation skipped")
    exit()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # replace 'server' with your project name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully")
else:
    print("Superuser already exists or environment variables missing")
