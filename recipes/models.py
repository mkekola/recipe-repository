from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title