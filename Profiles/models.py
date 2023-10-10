from django.db import models
from Images.models import Images, get_default_image
from django.core.validators import MinLengthValidator
import uuid

default_image = get_default_image

class Profiles(models.Model):
    profile_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
    )
    first_name = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255,
        unique=False
        )
    middle_name = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255, 
        unique=False, 
        default=''
        )
    last_name = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=255, 
        unique=False
        )
    description = models.TextField(default='')
    image = models.ForeignKey(Images, default=default_image, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.profile_id}'
    
    def get_profile(self):
        result = {
            'first_name': self.first_name, 
            'middle_name': self.middle_name, 
            'last_name': self.last_name, 
            'description': self.description, 
            'image': self.image.get_image_url()
        }
        return result
    
    def delete(self):
        self.image.delete()
        super(Profiles, self).delete()