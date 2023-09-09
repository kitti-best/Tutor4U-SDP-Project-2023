from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from django_password_validators.password_character_requirements.password_validation import PasswordCharacterValidator
from django.db.models import Q
from django.core.exceptions import ValidationError
from User.models import UserModel


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
        except ValidationError:
            return


class LoginSerializer(serializers.Serializer):
    
    def check_user(self, validated_data: dict):
        try:
            email=validated_data.get('email', None)
            username=validated_data.get('username', None)
            password=validated_data.get('password', None)
            
            user = UserModel.objects.filter(Q(email=email) | Q(username=username)).first()
            
            if (user is None):
                raise AuthenticationFailed({ 'message': 'User not found' })
            if (not user.is_active):
                raise AuthenticationFailed({ 'message': 'User are not activate' })
            if (not user.check_password(password)):
                raise AuthenticationFailed({ 'message': 'Password incorrect' })
            
            return user
        except ValidationError:
            raise AuthenticationFailed({ 'message': 'Invalid Input' })


class LogoutSerializer(serializers.Serializer):
    
    def sign_out(self, data: dict):
        pass
    