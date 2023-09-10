from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from abc import ABC
from .models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        # fields = '__all__'


class ViewSelfProfile(APIView, ABC):
    def get(self, request, username):
        user = get_object_or_404(UserModel, username=username)
        user = UserModelSerializer(user)
        return JsonResponse(user.data, status=status.HTTP_200_OK)


class Index(APIView, ABC):
    def get(self, request):
        return HttpResponse("Index is Working!!")

