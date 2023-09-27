from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from django_password_validators.password_character_requirements.password_validation import PasswordCharacterValidator
from django.db.models import Q
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from User.models import UserModel

from utils.token_manager import TokenManager


pwd_validator = PasswordCharacterValidator(
    min_length_digit=5, 
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


class LogoutAllSerializer(serializers.Serializer):

    def check_token(self, validated_data):
        try:
            token = validated_data.get('Authorization', None)
            if (token is None):
                raise NotAuthenticated(
                    {'message': '\'refresh_token\' not found'})

            if (token.startswith('Bearer ')):
                token_data = TokenManager.extract(
                    token.removeprefix('Bearer '))

            if (token_data is None):
                raise NotAuthenticated(
                    {'message': 'Token is invalid or expired'})

            _uuid = token_data.get('_uuid', None)
            user = UserModel.objects.filter(_uuid=_uuid).first()

            if (user is None):
                raise NotAuthenticated({'message': 'User not found'})

            tokens = OutstandingToken.objects.filter(user=user._uuid)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return user
        except Exception as error:
            raise NotAuthenticated({'message': str(error)})


class LoginSerializer(serializers.Serializer):

    def check_user(self, request, validated_data):
        try:
            email = validated_data.get('email', None)
            username = validated_data.get('username', None)
            password = validated_data.get('password', None)
            print(email, username, password)
            user = UserModel.objects.filter(
                Q(email=email) | Q(username=username)).first()
            print(user)
            if (user is None or not user.check_password(password)):
                raise AuthenticationFailed({'message': 'User or password invalid'})
            if (not user.is_active):
                raise AuthenticationFailed(
                    {'message': 'User are not activate'})
            return authenticate(
                request=request,
                username=user.username,
                password=password
            )
        except ValidationError:
            raise AuthenticationFailed({'message': 'Invalid Input'})


class TokenGenaratorSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['_uuid'] = user._uuid.hex
        return token
