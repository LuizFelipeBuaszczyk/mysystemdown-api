from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
class User(AbstractUser):
    username = None
    
    id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False
    )
    
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    previous_password = models.CharField(max_length=128, null=True)
    password_change_at = models.DateTimeField(null=True)

    USERNAME_FIELD = "email" # Informa que o Campo de login é o email
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email