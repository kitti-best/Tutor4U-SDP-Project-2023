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

class ChangeLearningCenterStatus(APIView):
    permission_classes = 'LearningCenter.approvable'

    def post(self, request, name, status):
        LC_STATUS = (
            ('waiting', 'waiting'),
            ('approve', 'approve'),
            ('reject', 'reject')
        )
        if status not in LC_STATUS:
            return Response({'message': 'please enter valid status'})
        
        try:
            learning_center = LearningCenter.objects.get(name=name)
        except:
            learning_center = None
        
        if learning_center is not None:
            learning_center.update_status()
            learning_center.save()
            return Response({'message': 'status updated'})
        return Response({'message': 'failed to update'})