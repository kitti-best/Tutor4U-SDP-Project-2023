from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LearningCenter
from .serializers import LearningCenterSerializer
from abc import ABC, abstractmethod

class ManageLearningCenter(APIView):
    def post(self, request):
        serializer = LearningCenterSerializer(data=request.data)

        print("something!")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchLearningCenter(APIView, ABC):
    @abstractmethod
    def get(self, request):
        pass
class SearchNameLearningCenter(SearchLearningCenter):
    def get(self, request):
        name = self.request.query_params.get('name', '')
        
        learning_centers = LearningCenter.objects.filter(name__icontains=name)
        serializer = LearningCenterSerializer(learning_centers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)