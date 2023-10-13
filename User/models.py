from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from Profiles.models import Profiles
import uuid

class UserModel(AbstractUser):

    user_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
    )
    username = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=150, 
        unique=True
    )
    password = models.CharField(
        validators=[MinLengthValidator(8)], 
        max_length=255, 
        unique=False,
        null=False
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = None
    last_name = None
    
    coins = models.BigIntegerField(default=10, editable=True, unique=False)
    phone = models.CharField(
        max_length=30, 
        default='', 
        validators=[RegexValidator(
            regex="((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))"
            )]
        )
    
    def __str__(self):
        return self.username
    
    def activate(self):
        self.is_active = True
    
    def delete(self):
        self.profile.delete()
        super(UserModel, self).delete()
