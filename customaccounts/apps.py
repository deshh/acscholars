from django.apps import AppConfig


class CustomAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customaccounts'

    def ready(self):
        import customaccounts.signals  # This ensures the signals are registered