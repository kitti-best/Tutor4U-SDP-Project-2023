from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from abc import ABC
from .forms import CustomUserForm
from .models import UserModel
from .serializer import UserModelSerializer
from Images.models import Images


class ViewSelfProfile(APIView, ABC):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user = UserModelSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)
    


class EditUserProfile(APIView):
    # @login_required (use this if want to make user login first to access this also use: from django.contrib.auth.decorators import login_required)
    def edit_profile(request):
        if request.method == 'POST':
            form = CustomUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return Response(status=status.HTTP_200_OK)


class Index(APIView, ABC):
    def get(self, request):
        return Response("Index is Working!!")

