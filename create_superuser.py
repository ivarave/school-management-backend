import os
import django

if os.environ.get("CREATE_SUPERUSER", "False") != "True":
    print("Superuser creation skipped")
    exit()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "User")

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    print("Superuser created successfully")
else:
    print("Superuser already exists or environment variables missing")
