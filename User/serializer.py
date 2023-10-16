from rest_framework import serializers
from .models import UserModel
from Profiles.serializers import ProfileSerializer


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'profile', 'phone', 'coins')
    
    @property
    def data(self):
        data = super().data
        user = self.instance
        
        profile = user.profile
        if profile:
            data.pop("profile")
            data.update({
                "first_name": profile.first_name, 
                "middle_name": profile.middle_name,
                "last_name": profile.last_name,
                "description": profile.description, 
                "image": profile.image.get_image_url(),
            })
            
        return data
