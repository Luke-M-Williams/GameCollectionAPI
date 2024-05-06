from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)  # For example, 'PlayStation', 'Xbox', 'PC', etc.

class Game(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name='games')  # Tags representing platforms or other categorizations