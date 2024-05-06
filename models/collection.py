from django.db import models
from .game import Game
from django.contrib.auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='collections')