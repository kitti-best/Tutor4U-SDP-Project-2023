from django.db import models
from django.conf import settings
import os
import uuid
import environ

env = environ.Env()
environ.Env.read_env()

def hash_upload(instance, filename):
    return f'media/images/{instance.image_id}_{filename}'

def get_default_image():
    default_id = '9a4b5d5d-01bd-493c-a143-2f8305dd2b35'
    default_image = Images.objects.filter(image_id=default_id).first()
    if default_image is None:
        image = Images(
            image_id=default_id, 
            image_file='media/images/default_image.png'
        )
        image.save()
        default_image = image
    return default_image.image_id

class Images(models.Model):
    default_id = '9a4b5d5d-01bd-493c-a143-2f8305dd2b35'
    image_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True)
    image_file = models.ImageField(
        upload_to=hash_upload, 
        height_field=None, 
        width_field=None, 
        default='media/images/default_image.png')
    
    def get_image_url(self):
        return self.image_file.url
    
    def delete(self):
        if str(self.image_id) != self.default_id:
            self.image_file.delete()
            super(Images, self).delete()
    
    def __str__(self):
        return f'{self.image_id}'
