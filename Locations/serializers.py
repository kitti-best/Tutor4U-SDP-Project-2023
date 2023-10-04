from rest_framework import serializers
from .models import Locations

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'