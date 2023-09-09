from rest_framework import serializers
from .models import LearningCenter

class LearningCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'