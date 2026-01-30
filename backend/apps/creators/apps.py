from django.apps import AppConfig


class CreatorsConfig(AppConfig):
    name = 'apps.creators'

    def ready(self):
        import apps.creators.signals  # noqa

