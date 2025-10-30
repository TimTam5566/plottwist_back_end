from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    GENRE_CHOICES = [
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Modern Drama', 'Modern Drama'),
        ('Historical', 'Historical'),
        ('Comedy', 'Comedy'),
        ('Childrens Fiction', "Children's Fiction"),
        ('Fantasy/Mythology', 'Fantasy/Mythology'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(
        max_length=30,  # Increase max_length if needed
        choices=GENRE_CHOICES,
        default='Thriller'
    )
    goal = models.IntegerField(
        help_text='Maximum number of contributions allowed',
        validators=[
            MinValueValidator(1, message='Must allow at least 1 contribution'),
            MaxValueValidator(100, message='Cannot exceed 100 contributions')
        ]
    )
    image = models.CharField(
        max_length=300,
        blank=True,
        help_text='Project cover image URL (optional)'
    )
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    starting_content = models.TextField()

    def __str__(self):
        return self.title

class Pledge(models.Model):
    amount = models.IntegerField(
        help_text='Number of verses/paragraphs contributed',
        validators=[
            MinValueValidator(1, message='Must contribute at least 1 verse/paragraph'),
            MaxValueValidator(20, message='Cannot exceed 10 verses/paragraphs per contribution')
        ]
    )
    comment = models.TextField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )
    add_content = models.TextField()

    def __str__(self):
        return f"{self.supporter} contributed {self.amount} to {self.project}"