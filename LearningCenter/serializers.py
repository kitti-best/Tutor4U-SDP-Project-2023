from rest_framework import serializers
from .models import LearningCenter


class LearningCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LearningCenterStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('students')


class LearningCenterTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('tutor')
