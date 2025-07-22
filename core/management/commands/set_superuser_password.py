from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Set superuser password from env if it exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("⚠️ Missing superuser credentials in env")
            return

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write("✅ Superuser password set successfully")
        except User.DoesNotExist:
            self.stdout.write(f"❌ No user with username '{username}' exists")
