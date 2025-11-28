from django.apps import AppConfig
# You may need to import your signals here or in ready()
# Let's keep the standard structure

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging' # App name must match the folder name

    def ready(self):
        # We need this to register the signals!
        # The relative import should work fine once the app is loaded as 'messaging'.
        try:
            from . import signals 
        except ImportError as e:
            # You can add a print statement here to see if the signals file is the issue.
            print(f"Error loading signals: {e}")
            pass