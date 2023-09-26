from rest_framework import serializers
from .models import LearningCenter, Tutor


class LearningCenterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        exclude = ('_uuid', 'owner')


class LearningCenterStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('students',)


class LearningCenterTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
