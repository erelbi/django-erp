from django.apps import AppConfig

class ERP(AppConfig):
    name = 'home'

    def ready(self):
        import home.signals