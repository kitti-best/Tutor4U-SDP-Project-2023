from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from .serializer import UserSerializer
from .models import CustomUser
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.urls import reverse


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        user.active()
        user.save()
        url = 'https://www.google.com'
        return HttpResponseRedirect(redirect_to=url)
    else: # error
        error_url = 'https://www.google.com'
        return HttpResponseRedirect(redirect_to=error_url)


def activateEmail(request, user):
    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'username': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    # message = f"Hi {data['username']},\n\nPlease click on the link below to confirm your registration:\n\n{'https' if request.is_secure() else 'http'}://{get_current_site(request).domain}"
    email = EmailMessage(mail_subject, message, to=[user.email])
    if not email.send():
        return False
    return True

class UserAuthViewSet(APIView):
    
    def post(self, request):
        data = request.data.get('data')
        password = data['password']
        data['password'] = make_password(data['password'])
        try:
            user = CustomUser.objects.get(email=data['email'])
            if user.check_password(password):
                activateEmail(request, user)
                return Response({'message': 'resend activation email'})
            else:
                return Response({'message': 'password mismatch'})
            
        except CustomUser.DoesNotExist:
            serializer = UserSerializer(data=data)
            if (serializer.is_valid(raise_exception=True)):
                saved = serializer.save()
            activateEmail(request, saved)
            return Response({
                'message': 'success',
            }, status=status.HTTP_201_CREATED)


class EmailLogin(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        
        serializer = UserSerializer
        
        data = request.data.get()
        username = data['username']
        password = data['password']
        
        user = CustomUser.objects.get(username=username)
        if (user is None):
            pass
    
    def __login(self):
        pass
    
    def generate_token(self):
        pass
    
    