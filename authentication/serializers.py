from rest_framework import serializers
from django.contrib.auth import authenticate
from django_password_validators.password_character_requirements.password_validation import PasswordCharacterValidator
from django.core.exceptions import ValidationError
from User.models import UserModel
from abc import ABC, abstractmethod

pwd_validator = PasswordCharacterValidator(
    min_length_digit=8,
    min_length_alpha=2,
    min_length_special=1,
    min_length_lower=1,
    min_length_upper=1,
    special_characters='-~!@#$%^&*()_+{}\":;\'[]'
)

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data: dict):
        try:
            self.error = ''
            password = validated_data.get('password', None)
            pwd_validator.validate(password)
            
            user = self.Meta.model(
                email=validated_data.get('email', None), 
                username=validated_data.get('username', None), 
                first_name=validated_data.get('first_name', None), 
                last_name=validated_data.get('last_name', None), 
            )
            user.set_password(password)
            user.save()
            
            return user
        except ValidationError as error:
            self.error = error

class LoginSerializer(serializers.Serializer):
    
    class Meta:
        model = UserModel
        fields = (
            'email', 
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


    def check_user(self, validated_data: dict):
        try:
            user = authenticate(
                username=validated_data.get('email', None), 
                password=validated_data.get('password', None)
            )
            return user
        except ValidationError as error:
            raise serializers.ValidationError({'message': error.message})