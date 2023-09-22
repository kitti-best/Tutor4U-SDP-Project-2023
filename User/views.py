from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from abc import ABC
from .models import UserModel
from .serializer import UserModelSerializer


class ViewSelfProfile(APIView, ABC):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user = UserModelSerializer(user)
        return JsonResponse(user.data, status=status.HTTP_200_OK)


class Index(APIView, ABC):
    def get(self, request):
        return Response("Index is Working!!")

