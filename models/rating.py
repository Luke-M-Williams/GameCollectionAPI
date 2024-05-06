from django.db import models
from .game import Game
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)

    class Meta:
        unique_together = ('user', 'game')