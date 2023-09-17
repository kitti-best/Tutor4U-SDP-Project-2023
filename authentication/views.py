from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from User.models import UserModel
from authentication.serializers import pwd_validator

from .serializers import RegisterSerializer, LoginSerializer, LogoutAllSerializer
from abc import ABC, abstractmethod
from utils.token_manager import TokenManager
import environ

env = environ.Env()
environ.Env.read_env()

class ResetPassword(APIView):
    def post(request, uidb64, token, password):
        error_url = 'https://www.google.com'
        url = 'https://www.google.com'
        
        try:
            pwd_validator.validate(password=password)
        except:
            return HttpResponseRedirect(redirect_to=error_url)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(_uuid=uid)
        except:
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(redirect_to=url)
        else: # error
            return HttpResponseRedirect(redirect_to=error_url)

class ResetPasswordSender(APIView):
    def post(request, email):
        try:
            user = UserModel.objects.get(email=email)
        except:
            user = None
        if user is not None:
            mail_subject = "Rest your password."
            message = render_to_string("reset_password.html", {
                'username': user.username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user._uuid)),
                'token': PasswordResetTokenGenerator().make_token(user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            if not email.send():
                return Response({'message': 'problem sending email'})
            return Response({'message': 'reset password email sended'})
        return Response({'message': 'email not found'})

class EmailActivation(APIView):
    def post(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(_uuid=uid)
        except:
            user = None
        
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.active()
            user.save()
            url = 'https://www.google.com'
            return HttpResponseRedirect(redirect_to=url)
        else: # error
            error_url = 'https://www.google.com'
            return HttpResponseRedirect(redirect_to=error_url)

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

    def activateEmail(request, user):
        mail_subject = "Activate your user account."
        message = render_to_string("activate_account.html", {
            'username': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user._uuid)),
            'token': PasswordResetTokenGenerator().make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        
        email = EmailMessage(mail_subject, message, to=[user.email])
        if not email.send():
            return False
        return True
    
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


class LoginAPIViews(LoginBase):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid(raise_exception=True)):
            user = serializer.check_user(request, data)
        
        access_token, refresh_token = TokenManager.generate(user)
        response = Response(
                {
                    'message': 'Login success', 
                    'access_token': access_token
                }, 
                status=status.HTTP_200_OK,
            )
        response.set_cookie(
            key='refresh_token', 
            value=refresh_token, 
            httponly=True, 
            secure =(env('NODE_ENV') == 'production')
        )
        return response


class LogoutAPIViews(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        try:
            cookies = request.COOKIES
            refresh_token = cookies.get('refresh_token', None)
            if (refresh_token is None):
                return Response(
                    { 'message': '\'refresh_token\' not found' }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response(
                    { 'message': 'Logout' }, 
                    status=status.HTTP_205_RESET_CONTENT
                )
            for cookie in cookies.keys():
                response.delete_cookie(cookie)
            
            return response
        except Exception as error:
            return Response(
                    { 'message': str(error) }, 
                    status=status.HTTP_400_BAD_REQUEST
                )


class LogoutAllAPIViews(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LogoutAllSerializer
    
    def post(self, request):
        headers = request.headers
        cookies = request.COOKIES
        serializer = self.serializer_class(data=headers)
        if (serializer.is_valid(raise_exception=True)):
            _ = serializer.check_token(headers)

        response = Response(
                {
                    'message': 'Logout success', 
                }, 
                status=status.HTTP_205_RESET_CONTENT,
            )
        for cookie in cookies.keys():
            response.delete_cookie(cookie)
        
        return response
