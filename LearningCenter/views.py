from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LearningCenter, Student, Tutor
from .serializers import LearningCenterSerializer, LearningCenterStudentSerializer
from abc import ABC, abstractmethod
from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404

class ViewLearningCenterInformation(APIView):
    def get(self, request, name):
        learning_center = get_object_or_404(LearningCenter, name=name)
        learning_center = LearningCenterSerializer(learning_center)
        return Response(learning_center.data, status=status.HTTP_200_OK)


class ViewLearningCenterStudentInformation(APIView):
    def get(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center = LearningCenterSerializer(learning_center)
        return Response(learning_center.data, status=status.HTTP_200_OK)
        learning_center_student = LearningCenterStudentSerializer(learning_center)
        return Response(learning_center_student.data, status=status.HTTP_200_OK)

from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required

# unfi
class AddStudentToLearningCenter(APIView):
    '''
    {
        "name": "on c mand",
        "description": "The best learning center in the world on mand"
    }
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        new_student = Student(**data)
        new_student.save()


# unfi
class AddTutorToLearningCenter(APIView):
    def post(self, request):
        data = request.data
        new_learning_center = Student(**data)
        new_learning_center.save()


class ViewLearningCenterTutorInformation(APIView):
    def get(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center_tutor = LearningCenterStudentSerializer(learning_center)
        return Response(learning_center_tutor.data, status=status.HTTP_200_OK)


class ManageLearningCenter(APIView):
    def post(self, request):
        serializer = LearningCenterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchLearningCenter(APIView, ABC):
    def get(self, request):
        name = self.request.query_params.get('name', '')
        levels = self.request.query_params.get('level', '').split(',')
        subjects_taught = self.request.query_params.get('subjects_taught', '').split(',')

        result_learning_centers = self.search_learning_centers(name, levels, subjects_taught)
        serializer = LearningCenterSerializer(result_learning_centers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def search_learning_centers(self, name, levels, subjects_taught):
        # Query use for complex queries
        query = Q()

        if name:
            query |= Q(name__icontains=name)

        for level in levels:
            query &= Q(levels__icontains=level.strip())

        for subject in subjects_taught:
            query &= Q(subjects_taught__icontains=subject.strip())
            
        query &= Q(status='approve')

        queryset = LearningCenter.objects.filter(query).order_by('-popularity')

        return queryset

class LearningCenterDefaultPendingPage(APIView):
    def get(self, request):
        if not request.user.has_perm('LearningCenter.learning_center_admin'):
            return Response(
                {'message': 'user doesn\'t have permission'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            result = LearningCenter.objects.filter(status='waiting').order_by('date_created')
            serializer = LearningCenterSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {'message': 'Failed to retrieve data'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class ChangeLearningCenterStatus(APIView):
    # permission_required  = 'LearningCenter.approvable'

    def post(self, request):
        LC_STATUS = (
            'waiting',
            'approve',
            'reject'
        )

        if not request.user.has_perm('LearningCenter.learning_center_admin'):
            return Response(
                {'message': 'user doesn\'t have permission'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data
        if data.get('status', None) not in LC_STATUS:
            return Response(
                {'message': 'please enter valid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            learning_center = LearningCenter.objects.get(name=data.get('name', None))
        except:
            learning_center = None
        
        if learning_center is not None:
            learning_center.update_status(data.get('status'))
            learning_center.save()
            return Response(
                {'message': 'status updated'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'cannot find learning center with this name'},
            status=status.HTTP_400_BAD_REQUEST
        )
