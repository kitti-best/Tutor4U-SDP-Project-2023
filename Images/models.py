from django.db import models
import uuid
import os
import environ

env = environ.Env()
environ.Env.read_env()


class Images(models.Model):
    image_id = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    image_file = models.ImageField(upload_to='images/', height_field=None, width_field=None, default='')

    @staticmethod
    def get_default_image():
        default_image = Images.objects.filter(image_id='9a4b5d5d-01bd-493c-a143-2f8305dd2b35').first().image_id
        print(default_image, type(default_image))
        return default_image
    
    def get_image_url(self):
        return f'https://{env("HOST")}:{env("PORT")}/{self.image_file.url}'
    
    def delete(self):
        os.remove(self.image_file.path)
        self.image_file.delete()
        super(Images, self).delete()
    
    def __str__(self):
        return f'{self.image_id}'
