from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LearningCenter, Location
from .serializers import LearningCenterSerializer
from abc import ABC, abstractmethod
from django.db.models import Q
from django.shortcuts import get_object_or_404
import math


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

        queryset = LearningCenter.objects.filter(query).order_by("-rating")

        return queryset

class LearningCenterDistanceFilter(APIView):
    def get(self, request):
        # Get the user's latitude and longitude from the request (you can customize this part)
        user_latitude = float(request.query_params.get('lat'))
        user_longitude = float(request.query_params.get('lon'))
        
        # Maximum distance in kilometers
        max_distance_km = float(request.query_params.get('max_distance', 5))

        # Filter Learning Centers within the specified distance
        learning_centers = self.filter_learning_centers_in_distance(
            user_latitude, user_longitude, max_distance_km
        )

        # Serialize and return the filtered Learning Centers
        serializer = LearningCenterSerializer(learning_centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_learning_centers_in_distance(self, lat, lon, max_distance_km=5):
        learning_centers = LearningCenter.objects.all()
        filtered_centers = []

        user_location = (lat, lon)

        for center in learning_centers:
            center_location = (center.latitude, center.longitude)
            distance = self.vector_distance(*user_location, *center_location)

            if distance <= max_distance_km:
                filtered_centers.append(center)

        return filtered_centers

    def vector_distance(self, lat1, lon1, lat2, lon2):
        earth_radius = 6371.0
        constant_pi = math.pi
        lat1_rad = lat1 * (constant_pi / 180.0)
        lon1_rad = lon1 * (constant_pi / 180.0)
        lat2_rad = lat2 * (constant_pi / 180.0)
        lon2_rad = lon2 * (constant_pi / 180.0)

        d_lat = lat2_rad - lat1_rad
        d_lon = lon2_rad - lon1_rad

        a = (math.sin(d_lat / 2))**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(d_lon / 2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = earth_radius * c

        return distance


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

class ManageLocation(APIView):
    def post(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            location = Location.objects.create(
            )

            learning_center.location = location
            learning_center.save()

            return Response({"message": "Location created and associated with Learning Center."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            if learning_center.location:
                learning_center.location.save()

                return Response({"message": "Location for Learning Center updated."})
            else:
                return Response({"error": "Learning Center does not have an associated location."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, learning_center_name):
        try:
            learning_center = get_object_or_404(LearningCenter, name=learning_center_name)

            if learning_center.location:
                learning_center.location.delete()

                learning_center.location = None
                learning_center.save()

                return Response({"message": "Location for Learning Center deleted."})
            else:
                return Response({"error": "Learning Center does not have an associated location."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)