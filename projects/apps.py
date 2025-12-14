'''
Apps configuration for the projects app.
'''

from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # BigAutoField = auto-incrementing ID that can handle HUGE numbers
    # IDs will be: 1, 2, 3, 4... up to 9,223,372,036,854,775,807
    name = 'projects'
    # The name of this app

    def ready(self):
        import projects.signals

        """
        When Django starts up and this app is "ready", import the signals module.
        
        SIGNALS are like "event listeners" in Django.
        They let you run code automatically when certain things happen.
        
        Example: "When a new pledge is created, automatically update the project's current_content"
        
        """