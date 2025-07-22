from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # def ready(self):
    #     # Optional: if you still use signals
    #     import core.signals

    #     self.create_superuser_on_startup()

    def create_superuser_on_startup(self):
        from django.db.utils import OperationalError
        try:
            User = get_user_model()
            username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

            user = User.objects.filter(username=username).first()
            if user and password and not user.check_password(password):
                user.set_password(password)
                user.save()
                print("✅ Superuser password set")
        except OperationalError:
            print("⚠️ DB not ready for setting superuser password")
