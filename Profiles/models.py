from django.db import models
from Images.models import Images
from django.core.validators import MinLengthValidator
import uuid

default_image = Images.get_default_image()

class Profiles(models.Model):
    profile_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
    )
    firstname = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255,
        unique=False
        )
    middlename= models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255, 
        unique=False, 
        default=''
        )
    lastname = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255, 
        unique=False
        )
    description = models.TextField(default='')
    image = models.ForeignKey(Images, default=default_image, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.profile_id}'
