from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    is_private = models.BooleanField(default=False)
    access_code = models.CharField(max_length=128, blank=True) # FLAW 5: Storing access codes in plaintext
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class LoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    failed_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('username', 'ip_address')

    def __str__(self):
        return f"{self.username} - {self.ip_address}"