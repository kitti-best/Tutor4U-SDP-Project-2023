from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import LearningCenter
from .serializer import LearningCenterSerializer


class ViewLearningCenterInformation(APIView):
    def get(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center = LearningCenterSerializer(learning_center)
        return Response(learning_center.data, status=status.HTTP_200_OK)

