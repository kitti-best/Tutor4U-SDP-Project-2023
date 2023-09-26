from rest_framework import serializers
from .models import LearningCenter, Tutor


class LearningCenterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LearningCenterStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LearningCenterTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
