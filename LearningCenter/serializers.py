from rest_framework import serializers
from .models import LearningCenter, Tutor


class LearningCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LearningCenterStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('students')


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
