from django.apps import AppConfig

class HomeConfig(AppConfig):  # Replace 'Home' with your app's name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'  # Replace with your app's name
    
    def ready(self):
        import home.templatetags.dsc_extras  # Force registration
    # def ready(self):
    #     import home.signals  # Ensure the signals are imported
