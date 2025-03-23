from django.apps import AppConfig

class LibraryConfig(AppConfig):
    """
    Configuration for the Library app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        """
        Import signals or perform startup tasks when the app is ready.
        """
        import library.signals  # Optional: For custom signals (if needed)
