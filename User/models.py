from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
import uuid

class UserModel(AbstractUser):
    _uuid = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
    )
    email = models.EmailField(unique=True)
    username = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=150, 
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        blank=False
    )
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def activate(self):
        self.is_active = True
