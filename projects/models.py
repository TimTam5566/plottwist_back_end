from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.CharField(max_length=300, blank=True)
    genre = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    starting_content = models.TextField(blank=True, default='')  # <-- new field
    current_content = models.TextField(blank=True, default='')
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

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