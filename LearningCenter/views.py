from rest_framework import serializers, status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import LearningCenter


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = ('name', 'description', 'house_number', 'section',
                  'sub_district', 'district', 'province', 'country',
                  'website', 'phone_number', 'email', 'subjects_taught')


class ViewLearningCenterInformation(APIView):
    def get(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center = UserModelSerializer(learning_center)
        return JsonResponse(learning_center.data, status=status.HTTP_200_OK)
