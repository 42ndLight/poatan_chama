from django.apps import AppConfig

class CashpoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cashpool'

    def ready(self):
        from . import signals 
    