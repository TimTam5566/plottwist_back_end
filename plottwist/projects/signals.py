from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging
import json
from .models import Pledge

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pledge)
def append_pledge_to_project(sender, instance, created, **kwargs):
    """
    Signal handler that appends pledge content to the associated project
    when a new pledge is created.
    """
    if created and instance.project_id:
        try:
            with transaction.atomic():
                project = instance.project

                if not project:
                    logger.error("Project not found for pledge")
                    return

                logger.info(f"""
                    Processing pledge:
                    ID: {instance.id}
                    Project ID: {project.id}
                    Added Content: {instance.add_content}
                """)

                # Append new content to starting_content
                new_line = instance.add_content.strip() if instance.add_content else None

                if new_line:
                    project.starting_content = (project.starting_content or '').strip() + "\n" + new_line
                    logger.info(f"Added new line to project {project.id}")

                project.save()
                logger.info(f"Successfully updated project {project.id}")
        except Exception as e:
            logger.error(f"Error details: {str(e)}")
            logger.error(f"Pledge data: {json.dumps({
                'id': instance.id,
                'project_id': instance.project_id,
                'add_content': instance.add_content
            }, indent=2)}")
            raise
