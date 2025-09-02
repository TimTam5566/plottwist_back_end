from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    genre = models.TextField()
    poemstart = models.TextField()
    storystart = models.TextField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(
        auto_now_add=True
        )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    poemline = models.TextField()
    storyverse = models.TextField()
    comment = models.TextField()
    anonymous = models.BooleanField()
    supporter = models.CharField(max_length=200)
    project = models.ForeignKey(
        'Pledge',
        on_delete=models.CASCADE,
        related_name='pledges', 
        )
    date_created = models.DateTimeField(
        auto_now_add=True
        )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )