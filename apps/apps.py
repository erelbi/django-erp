from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'home'

    def ready(self):
        import home.signals