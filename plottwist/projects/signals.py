from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Pledge, Project

@receiver(post_save, sender=Pledge)
def append_pledge_to_project(sender, instance, created, **kwargs):
    """
    Signal handler that appends pledge content (poem line or story verse) to the associated project
    when a new pledge is created.

    Args:
        sender: The model class (Pledge)
        instance: The actual Pledge instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional arguments passed by the signal
    """
    if created and instance.project_id:
        try:
            with transaction.atomic():
                project = instance.project

                # Append new lines to existing content
                if instance.poemline:
                    project.poemstart = (project.poemstart or '').strip() + "\n" + instance.poemline.strip()
                if instance.storyverse:
                    project.storystart = (project.storystart or '').strip() + "\n" + instance.storyverse.strip()

                project.save()
        except Exception as e:
            # Log the error - in a production environment, you would want to use proper logging
            print(f"Error updating project with pledge content: {str(e)}")
