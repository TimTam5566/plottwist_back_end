"""
    Models.py is the database blueprint
        for the CustomUser in our Django application.
    This is the User model - it defines what a "user" looks like in your database.
    
    Why use CUSTOMUSER instead of the default User model?
    Django comes with a built-in User model, but it's best practice to create
    your own from the start. This way, if you ever want to add extra fields
    (like profile_picture, bio, date_of_birth), you can easily do it.
    
    Basic model fields included:
    - username
    - email
    - password (automatically hashed/encrypted)
    - first_name, last_name
    - is_active, is_staff, is_superuser
    - date_joined, last_login
    
    
    """


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    def __str__(self):
    # This controls what shows up when you print a user or see them in Django Admin
        return self.username
    
