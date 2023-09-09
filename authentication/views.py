from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from .serializers import RegisterSerializer, LoginSerializer
from abc import ABC, abstractmethod
from utils.token_generator import TokenManager as token
import jwt
import environ

env = environ.Env()
environ.Env.read_env()

class RegisterBase(APIView, ABC):
    permission_classes = (AllowAny, )
    
    @abstractmethod
    def post(self):
        raise NotImplementedError()

class LoginBase(APIView, ABC):
    permission_classes = (AllowAny, )
    
    @abstractmethod
    def post(self):
        raise NotImplementedError()

class EmailRegistrationAPIViews(RegisterBase):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid(raise_exception=True)):
            user = serializer.create(data)
        
        if (user is None):
            return Response(
                { 'message': serializer.errors }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
                { 'message': 'success' }, 
                status=status.HTTP_201_CREATED
            )


class EmailLoginAPIViews(LoginBase):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid(raise_exception=True)):
            user = serializer.check_user(data)
        
        login(request, user)
        username = user.username
        access_token = token.build(username=username, option='ACCESS')
        refresh_token = token.build(username=username, option='REFRESH')
        response = Response(
                {
                    'message': 'Login success', 
                    'username': username, 
                    'access_token': access_token
                }, 
                status=status.HTTP_200_OK
            )
        response.set_cookie(
            key='refresh_token', 
            value=refresh_token, 
            httponly=True, 
            secure =(env('NODE_ENV') == 'Production')
        )
        
        return response


class AdminLoginAPIViews(EmailLoginAPIViews):
    pass
    # def post(self, request):
    #     return super().post(self, request, self.is_super)
    
    # def is_super(user):
    #     return user.is_superuser
