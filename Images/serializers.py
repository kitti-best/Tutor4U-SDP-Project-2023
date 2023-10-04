from rest_framework import serializers
from Images.models import Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
