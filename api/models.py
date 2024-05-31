from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, error_messages={"unique": ("A user with that email already exists.")})
    
    def __str__(self) -> str:
        return self.email
    