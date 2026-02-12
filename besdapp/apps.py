from django.apps import AppConfig

class BesdappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'besdapp' # <--- Vérifiez que ce n'est pas 'backend' ici
    
    def ready(self):
        import besdapp.signals  # Importation cruciale pour activer les signaux