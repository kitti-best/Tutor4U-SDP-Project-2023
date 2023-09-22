from rest_framework import serializers
from .models import LearningCenter, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LearningCenterSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Nested Location serializer

    class Meta:
        model = LearningCenter
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        learning_center = LearningCenter.objects.create(location=location, **validated_data)
        return learning_center
