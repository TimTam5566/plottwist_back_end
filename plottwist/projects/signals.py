from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging
import json
from .models import Pledge  # Add this import

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pledge)
def append_pledge_to_project(sender, instance, created, **kwargs):
    """
    Signal handler that appends pledge content (poem line or story verse) to the associated project
    when a new pledge is created.
    """
    if created and instance.project_id:
        try:
            with transaction.atomic():
                project = instance.project
                
                if not project:
                    logger.error("Project not found for pledge")
                    return
                
                # Enhanced logging
                logger.info(f"""
                    Processing pledge:
                    ID: {instance.id}
                    Project ID: {project.id}
                    Poem Line: {instance.poemline}
                    Story Verse: {instance.storyverse}
                """)

                # Append new lines to existing content
                if instance.poemline:
                    project.poemstart = (project.poemstart or '').strip() + "\n" + instance.poemline.strip()
                    logger.info(f"Added poem line to project {project.id}")
                if instance.storyverse:
                    project.storystart = (project.storystart or '').strip() + "\n" + instance.storyverse.strip()
                    logger.info(f"Added story verse to project {project.id}")

                project.save()
                logger.info(f"Successfully updated project {project.id}")
        except Exception as e:
            logger.error(f"Error details: {str(e)}")
            logger.error(f"Pledge data: {json.dumps({
                'id': instance.id,
                'project_id': instance.project_id,
                'poemline': instance.poemline,
                'storyverse': instance.storyverse
            }, indent=2)}")
            raise
