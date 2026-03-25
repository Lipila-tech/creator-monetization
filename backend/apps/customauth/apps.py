from django.apps import AppConfig
import os
from django.conf import settings
from django.core.management import call_command

class CustomAuthConfig(AppConfig):
    name = "apps.customauth"

    def ready(self):
        from .firebase import initialize_firebase
        initialize_firebase()

        if os.environ.get("DJANGO_AUTO_SETUP", "false").lower() != "true":
            return
        if getattr(settings, "RUNNING_AUTO_SETUP", False):
            return
        settings.RUNNING_AUTO_SETUP = True
        #try:
         #   call_command("migrate", interactive=False, run_syncdb=True)
        #except Exception:
         #   pass
        try:
            call_command("collectstatic", "--noinput")
        except Exception:
            pass
