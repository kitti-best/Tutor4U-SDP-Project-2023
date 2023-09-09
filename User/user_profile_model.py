from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    username = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    contact_number = models.IntegerField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_tutor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.username
    
    def activate(self):
        self.is_active = True

    def create_tutor(self):
        self.is_tutor = True



    
