from rest_framework import serializers
from .models import LearningCenter


class LearningCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('name', 'description', 'house_number', 'section',
                  'sub_district', 'district', 'province', 'country',
                  'website', 'phone_number', 'email', 'subjects_taught')
