from rest_framework import serializers
from .models import LearningCenter, Locations, Tutor, Student
from Locations.serializers import LocationsSerializer

class LearningCenterInfoSerializer(serializers.ModelSerializer):
    location = LocationsSerializer()

    class Meta:
        model = LearningCenter
        fields = '__all__'
        
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Locations.objects.create(**location_data)
        learning_center = LearningCenter.objects.create(location=location, **validated_data)
        return learning_center


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
