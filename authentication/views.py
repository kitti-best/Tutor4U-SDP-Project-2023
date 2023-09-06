from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import RegisterSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from abc import ABC, abstractmethod

class RegisterBase(APIView, ABC):
    permission_classes = (AllowAny, )
    
    @abstractmethod
    def post(self):
        raise NotImplementedError()

class LoginBase(APIView, ABC):
    permission_classes = (AllowAny, )
    # authentication_classes = (JSONWebTokenAuthentication, )
    
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
                { 'detail': serializer.errors }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
                { 'detail': 'success' }, 
                status=status.HTTP_201_CREATED
            )


class EmailLoginAPIViews(LoginBase):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid(raise_exception=True)):
            user = serializer.check_user(data)
        
        if (user is None):
            return Response(
                { 'detail': serializer.errors }, 
                status=status.HTTP_403_FORBIDDEN
        )
        
        login(request, user)
        return Response(
                {
                    'detail': 'Login success', 
                    'user': user.username
                }, 
                status=status.HTTP_200_OK
            )


class AdminLoginAPIViews(EmailLoginAPIViews):

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = self._is_valid(serializer, data)

        if (user is not None and user.is_superuser):
            login(request, user)
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK
            )
        return Response(
            { 'detail': 'Access denied' }, 
            status=status.HTTP_403_FORBIDDEN
        )