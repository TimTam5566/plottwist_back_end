'''
signals.py is the automatic update mechanism for appending pledge 
content to projects upon pledge creation.

Instead of manually updating the project in every view that creates a pledge, 
the signal does it automatically. 

'''

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
    ============================================================
    WHAT IS A SIGNAL?
    ============================================================
    A signal is like an "event listener" in Django.
    
    This one says: "AFTER a Pledge is SAVED, run this function"
    
    @receiver(post_save, sender=Pledge) means:
    - post_save = after saving
    - sender=Pledge = only for Pledge model (not other models)
    
    ============================================================
    WHAT THIS DOES:
    ============================================================
    When someone creates a new pledge (contribution), this automatically
    appends their content to the project's starting_content.
    
    FLOW:
    1. User submits pledge with add_content = "The dragon roared!"
    2. Pledge is saved to database
    3. This signal FIRES automatically
    4. It finds the project and appends the new content
    5. Project.starting_content now includes the new contribution
    
    ============================================================
    PARAMETERS EXPLAINED:
    ============================================================
    sender = The model class (Pledge)
    instance = The actual pledge object that was just saved
    created = True if this is a NEW pledge, False if it's an update
    **kwargs = Other stuff we don't need
    """
    # Only run for NEW pledges (not updates)
    if created and instance.project_id:
        try:
            # transaction.atomic() = if anything fails, undo everything
            # This prevents partial/broken updates
            with transaction.atomic():
                project = instance.project # Get the related project

                if not project:
                    logger.error("Project not found for pledge")
                    return

                # Log what we're doing (helpful for debugging)
                logger.info(f"""
                    Processing pledge:
                    ID: {instance.id}
                    Project ID: {project.id}
                    Added Content: {instance.add_content}
                """)

                # Get the new content, strip whitespace
                new_line = instance.add_content.strip() if instance.add_content else None

                if new_line:
                    # APPEND the new content to starting_content
                    # (project.starting_content or '') handles if it's None
                    project.starting_content = (project.starting_content or '').strip() + "\n" + new_line
                    logger.info(f"Added new line to project {project.id}")

                project.save() # Save the updated project
                logger.info(f"Successfully updated project {project.id}")
        except Exception as e:
            logger.error(f"Error details: {str(e)}")
            logger.error(f"Pledge data: {json.dumps({
                'id': instance.id,
                'project_id': instance.project_id,
                'add_content': instance.add_content
            }, indent=2)}")
            raise # Re-raise the error so we know something failed
