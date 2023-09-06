from .models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = '__all__'

