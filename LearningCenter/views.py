from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LearningCenter
from .serializers import LearningCenterSerializer
from abc import ABC, abstractmethod
from django.db.models import Q
from django.shortcuts import get_object_or_404


class ViewLearningCenterInformation(APIView):
    def get(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center = LearningCenterSerializer(learning_center)
        return Response(learning_center.data, status=status.HTTP_200_OK)


class CreateLearningCenter(APIView):
    def post(self, request):
        serializer = LearningCenterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditLearningCenter(APIView):
    def put(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        serializer = LearningCenterSerializer(learning_center, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteLearningCenter(APIView):
    def delete(self, request, id):
        learning_center = get_object_or_404(LearningCenter, _uuid=id)
        learning_center.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchLearningCenter(APIView, ABC):
    def get(self, request):
        name = self.request.query_params.get("name", "")
        levels = self.request.query_params.get("level", "").split(",")
        subjects_taught = self.request.query_params.get("subjects_taught", "").split(
            ","
        )

        result_learning_centers = self.search_learning_centers(
            name, levels, subjects_taught
        )
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

        query &= Q(status="approve")

        queryset = LearningCenter.objects.filter(query).order_by("-popularity")

        return queryset


class ChangeLearningCenterStatus(APIView):
    permission_classes = "LearningCenter.approvable"

    def post(self, request, name, status):
        LC_STATUS = (
            ("waiting", "waiting"),
            ("approve", "approve"),
            ("reject", "reject"),
        )
        if status not in LC_STATUS:
            return Response({"message": "please enter valid status"})

        try:
            learning_center = LearningCenter.objects.get(name=name)
        except:
            learning_center = None

        if learning_center is not None:
            learning_center.update_status()
            learning_center.save()
            return Response({"message": "status updated"})
        return Response({"message": "failed to update"})

from django.http import JsonResponse
from .models import Location
class ManageLocation(APIView):
    def post(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            location = Location.objects.create(
            )

            learning_center.location = location
            learning_center.save()

            return JsonResponse({"message": "Location created and associated with Learning Center."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            if learning_center.location:
                learning_center.location.save()

                return JsonResponse({"message": "Location for Learning Center updated."})
            else:
                return JsonResponse({"error": "Learning Center does not have an associated location."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            if learning_center.location:
                learning_center.location.delete()

                learning_center.location = None
                learning_center.save()

                return JsonResponse({"message": "Location for Learning Center deleted."})
            else:
                return JsonResponse({"error": "Learning Center does not have an associated location."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)