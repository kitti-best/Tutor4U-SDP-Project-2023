from rest_framework import serializers
from User.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        # fields = '__all__'
