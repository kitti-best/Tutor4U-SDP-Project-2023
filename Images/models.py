from django.db import models
from django.conf import settings
import uuid
import os
import environ

import base64
from PIL import Image

env = environ.Env()
environ.Env.read_env()


class Images(models.Model):
    default_id = '9a4b5d5d-01bd-493c-a143-2f8305dd2b35'
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
        try:
            image_path = self.image_file.path
            buff = image_path.lower()
            
            header=''
            if buff.endswith('.png'):
                header = 'data:image/png;base64'
            elif buff.endswith('.jpg'):
                header = 'data:image/jpg;base64'
            elif buff.endswith('.jpeg'):
                header = 'data:image/jpeg;base64'
                
            with open(image_path, "rb") as image_file:
                data = str(base64.b64encode(image_file.read()))
            return f'{header},{data[2:-1]}'
        except:
            return ''
    
    def delete(self):
        if self.image_id != self.default_id:
            os.remove(self.image_file.path)
            self.image_file.delete()
            super(Images, self).delete()
    
    def save(self):
        self.image_file=self.hash_upload(self.image_file.path)
        super(Images, self).save()
    
    def hash_upload(self, filename):
        self.image_file.open() # make sure we're at the beginning of the file
        fname, ext = os.path.splitext(filename)
        return "{0}_{1}{2}".format(fname, uuid.uuid4(), ext)
        
    # def save(self):
    #     self.image_file = 'images/' + self
    #     super(Images, self).save()
        
    def __str__(self):
        return f'{self.image_id}'
