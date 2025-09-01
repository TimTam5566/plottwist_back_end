from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    genre = models.TextField()
    poemstart = models.TextField()
    storystart = models.TextField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)