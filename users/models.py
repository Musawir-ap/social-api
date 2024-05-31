from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # username = 
    email = models.EmailField(unique=True, null=False, error_messages={"unique": ("A user with that username already exists.")})
    
    def __str__(self) -> str:
        return self.email
    
    

    