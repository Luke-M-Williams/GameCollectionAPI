from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def get_default_user_id():
    # Assumes you have at least one user, typically an admin; otherwise, you'll need to handle this potential error
    return User.objects.first().id

from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=255)

class Game(models.Model):
    title = models.CharField(max_length=255)
    cover_art = models.URLField()
    genre = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    release_date = models.DateField()
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    platforms = models.ManyToManyField(Platform)  # This should be your many-to-many relationship

    def __str__(self):
        return self.title