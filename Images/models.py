from django.db import models
import uuid
import os
import environ

env = environ.Env()
environ.Env.read_env()


class Images(models.Model):
    image_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True)
    image_file = models.ImageField(
        upload_to='images/', 
        height_field=None, 
        width_field=None, 
        default='images/default_image.png')
    
    @staticmethod
    def get_default_image():
        default_id = '9a4b5d5d-01bd-493c-a143-2f8305dd2b35'
        default_image = Images.objects.filter(image_id=default_id).first()
        if default_image is None:
            image = Images(
                image_id=default_id, 
                image_file='images/default_image.png'
            )
            image.save()
            default_image = image
        return default_image.image_id
    
    def get_image_url(self):
        return f'https://{env("HOST")}:{env("PORT")}' + self.image_file.url
    
    def delete(self):
        os.remove(self.image_file.path)
        self.image_file.delete()
        super(Images, self).delete()
    
    def __str__(self):
        return f'{self.image_id}'
