'''
Database modelblueprint for projects.
'''

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================================
# CHOICES - Predefined options for dropdown fields
# ============================================================

CONTENT_TYPE_CHOICES = [
    ('story', 'Story'), # ('story/poem - stored in database',Story/Poem- readable/displayed on frontend')
    ('poem', 'Poem'),
]

# ============================================================
# PROJECT MODEL - A collaborative writing project
# ============================================================
class Project(models.Model):
    """
    A Project is a collaborative story or poem that users create.
    Think of it like a "Choose Your Own Adventure" book that multiple people write together.
    
    REAL-WORLD EXAMPLE:
    - Title: "The Mystery of the Haunted Lighthouse"
    - Description: "A spooky tale where readers decide what happens next"
    - Genre: "Horror"
    - Content Type: "Story"
    - The owner starts it, then others add "pledges" (contributions)
    """
    # ---- BASIC INFO ----
    title = models.CharField(max_length=200)
    # CharField = short text (limited characters)
    # max_length=200 means title can't exceed 200 characters
    description = models.TextField()
    # TextField = long text (unlimited length)
    # Used for the project summary/description
    goal = models.IntegerField()
    # IntegerField = whole number
    # This is the TARGET number of contributions the project wants
    # Example: goal=10 means they want 10 people to contribute
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    # ImageField = handles image uploads
    # upload_to='project_images/' = images saved in /media/project_images/
    # blank=True = form can be submitted without an image
    # null=True = database can store NULL (empty) for this field
    # Images handled by CLOUDINARY for 
        # I integrated Cloudinary for image storage because Heroku has an ephemeral filesystem - files disappear after 24 hours. 
        # I configured Django's STORAGES setting to automatically route all media uploads to Cloudinary. 
        # The frontend sends images via FormData, Django's ImageField handles validation, 
        # and the cloudinary-storage package transparently uploads to their CDN. 
        # The database only stores the URL, and images are served directly from Cloudinary's global CDN for fast loading. 🎉
    genre = models.CharField(max_length=100)
    # The category: "Horror", "Romance", "Sci-Fi", etc.
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='story') 
    # choices=CONTENT_TYPE_CHOICES = dropdown limited to 'story' or 'poem'
    # default='story' = if not specified, defaults to 'story'
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    """
    ForeignKey = "This project BELONGS TO one user"
    
    WHAT THIS CREATES:
    - Each project has ONE owner
    - Each user can have MANY projects
    - This is a "Many-to-One" relationship
    
    get_user_model() = gets your CustomUser model
    
    on_delete=models.CASCADE = "If the user is deleted, delete their projects too"
    Other options:
    - PROTECT = prevent deletion if projects exist
    - SET_NULL = set owner to NULL (would need null=True)
    """
    # ---- CONTENT FIELDS ----
    starting_content = models.TextField(blank=True, default='')
    # The ORIGINAL content the owner writes to start the story
    # This never changes - it's the foundation  
    current_content = models.TextField(blank=True, default="")
    # The FULL story including all contributions
    # This grows as people add pledges
    # Example flow:
    #   1. Owner creates project with starting_content = "Once upon a time..."
    #   2. current_content starts as "Once upon a time..."
    #   3. User A adds pledge: "A dragon appeared!"
    #   4. current_content becomes: "Once upon a time... A dragon appeared!"
    #   5. User B adds pledge: "The hero drew their sword."
    #   6. current_content becomes: "Once upon a time... A dragon appeared! The hero drew their sword."
    # ---- STATUS & TIMESTAMPS ----
    is_open = models.BooleanField(default=True)
    # BooleanField = True or False
    # True = project is accepting new contributions
    # False = project is closed/completed
    date_created = models.DateTimeField(auto_now_add=True)
    # DateTimeField = stores date AND time
    # auto_now_add=True = automatically set to NOW when created
    # This NEVER changes after creation

    def __str__(self):
        # What shows in Django Admin and when you print a project
        return self.title

# ============================================================
# PLEDGE MODEL - A contribution to a project
# ============================================================
class Pledge(models.Model):
    """
    A Pledge is someone's CONTRIBUTION to a project.
    In traditional crowdfunding, a pledge is money.
    In Plot Twist, a pledge is CONTENT (paragraphs or verses).
    
    REAL-WORLD EXAMPLE:
    - User "Sarah" contributes to "The Mystery of the Haunted Lighthouse"
    - She adds 2 paragraphs continuing the story
    - Her pledge: amount=2, add_content="The door creaked open slowly..."
    """
    amount = models.IntegerField(
        help_text='Number of verses/paragraphs contributed',
        validators=[
            MinValueValidator(1, message='Must contribute at least 1 verse/paragraph'),
            MaxValueValidator(20, message='Cannot exceed 20 verses/paragraphs per contribution')
        ]
    )
    """
    amount = how many paragraphs/verses they're adding
    
    validators = rules that must be followed:
    - MinValueValidator(1) = must be at least 1
    - MaxValueValidator(20) = can't be more than 20
    
    help_text = hint shown in forms/admin
    
    NOTE: There's a bug! The message says "cannot exceed 10" but validator is 20
    """
    comment = models.TextField()
    # A note from the contributor
    # Example: "I thought the story needed more suspense!"
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    """
    ForeignKey = "This pledge BELONGS TO one project"
    
    related_name='pledges' = THIS IS POWERFUL!
    It lets you do: project.pledges.all()
    Instead of: Pledge.objects.filter(project=project)
    
    Example:
        my_project = Project.objects.get(id=1)
        all_contributions = my_project.pledges.all()  # Get all pledges for this project
    """
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )
    """
    The USER who made this contribution
    
    related_name='supporter_pledges' lets you do:
        user.supporter_pledges.all()  # Get all pledges this user has made
    """
    add_content = models.TextField()
    # The ACTUAL CONTENT being contributed
    # This is the story text, poem verses, etc.
    # Example: "The dragon roared and flames lit up the night sky..."
    anonymous = models.BooleanField(default=False)
    # If True, the supporter's name is hidden from public view

    def __str__(self):
        return f"{self.supporter} contributed {self.amount} to {self.project}"