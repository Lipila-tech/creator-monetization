from django.apps import AppConfig


class WalletsConfig(AppConfig):
    name = 'apps.wallets'

    def ready(self):
        import apps.wallets.signals  # noqa
