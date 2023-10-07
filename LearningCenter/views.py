import http
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from Images.serializers import ImageSerializer
from Profiles.models import Profiles
from Profiles.serializers import ProfileSerializer
from .forms import CustomLearningCenterForm
from .models import LearningCenter, Student, Tutor, TutorImageForm, SubjectsTaught, Subjects, LearningCenterInteriors, LearningCenterLevels
from Images.models import Images
from .serializers import LearningCenterInfoSerializer, TutorSerializer

from abc import ABC
from uuid import UUID
import math

class Index(APIView):
    def get(self, request):
        tutors_data = []
        tutors = Tutor.objects.all()

        for tutor in tutors:
            tutor_data = TutorSerializer(tutor).data
            tutors_data.append(tutor_data)

        return '''render(request, 'view_images.html', {"tutors": tutors})'''


class ViewLearningCenterInformation(APIView):
    serializer_class = LearningCenterInfoSerializer
    
    def get(self, request, lcid):
        try:
            lcid = UUID(lcid, version=4)
        except ValueError:
            return Response({'message': 'Invalid Learning Center ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        learning_center = get_object_or_404(LearningCenter, learning_center_id=lcid)
        
        serializer = self.serializer_class(learning_center)
        response = serializer.data

        return Response(response, status=status.HTTP_200_OK)


class AddStudent(APIView):
    def post(self, request):
        data: dict = request.data
        # django append _id for foreignkey column
        # So we will remove the old one and replace with ones with _id instead
        learning_center = data.get('learning_center')
        if learning_center is None:
            return Response(status=http.HTTPStatus.NOT_FOUND)

        user = request.user
        # if user.user_id != learning_center.owner:
        #     return Response(status=http.HTTPStatus.UNAUTHORIZED)

        # change query object to normal dictionary
        data_as_dict = {}
        # dict is mutable so this work
        [data_as_dict.update({key: val}) for key, val in data.items()]

        image = Images(image_file=data_as_dict['image'])

        profile = Profiles(
            first_name=data_as_dict['first_name'],
            middle_name=data_as_dict['middle_name'],
            last_name=data_as_dict['last_name'],
            description=data_as_dict['description'],
            image=image
        )
        new_student = Student(profile=profile, learning_center_id=learning_center)

        image.save()
        profile.save()
        new_student.save()
        return Response(status=status.HTTP_200_OK)


class AddTutor(APIView):
    def post(self, request):
        data: dict = request.data
        # django append _id for foreignkey column
        # So we will remove the old one and replace with ones with _id instead
        learning_center = data.get('learning_center')
        if learning_center is None:
            return Response(status=http.HTTPStatus.NOT_FOUND)

        user = request.user
        # if user.user_id != learning_center.owner:
        #     return Response(status=http.HTTPStatus.UNAUTHORIZED)

        # change query object to normal dictionary
        data_as_dict = {}
        # dict is mutable so this work
        [data_as_dict.update({key: val}) for key, val in data.items()]

        image = Images(image_file=data_as_dict['image'])

        profile = Profiles(
            first_name=data_as_dict['first_name'],
            middle_name=data_as_dict['middle_name'],
            last_name=data_as_dict['last_name'],
            description=data_as_dict['description'],
            image=image
        )
        new_tutor = Tutor(profile=profile, learning_center_id=learning_center)

        image.save()
        profile.save()
        new_tutor.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        form = TutorImageForm()
        return render(request, "gallery.html", {"form": form})


class ViewStudents(APIView):
    def get(self, request, lcid):
        students_data = Student.objects.filter(learning_center=lcid).values()
        student_list = []
        for student in students_data:
            profile = Profiles.objects.get(profile_id=student['profile_id'])
            profile_json = ProfileSerializer(profile).data
            profile_image_id = profile_json['image']
            profile_image = Images.objects.get(image_id=profile_image_id)
            profile_image = ImageSerializer(profile_image).data
            profile_json['image'] = profile_image['image_file']
            profile_json.pop('profile_id')
            student_list.append(profile_json)
        return Response({"students": student_list}, status=status.HTTP_200_OK)


class ViewTutors(APIView):
    def get(self, request, lcid):
        tutors_data = Tutor.objects.filter(learning_center=lcid).values()
        tutor_list = []
        for tutor in tutors_data:
            profile = Profiles.objects.get(profile_id=tutor['profile_id'])
            profile_json = ProfileSerializer(profile).data
            profile_image_id = profile_json['image']
            profile_image = Images.objects.get(image_id=profile_image_id)
            profile_image = ImageSerializer(profile_image).data
            profile_json['image'] = profile_image['image_file']
            profile_json.pop('profile_id')
            tutor_list.append(profile_json)
        return Response({"tutors": tutor_list}, status=status.HTTP_200_OK)


class EditLearningCenter(APIView):
    # @login_required (use this if want to make user login first to access this also use: from django.contrib.auth.decorators import login_required)
    def post(request):
        form = CustomLearningCenterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return Response(status=status.HTTP_200_OK)


class ManageLearningCenter(APIView):
    def post(self, request):
        data = request.data
        subjects_taught = data.get('subjects_taught', [])
        levels = data.get('learning_center_levels', [])
        serializer = LearningCenterInfoSerializer(data=data)
        if serializer.is_valid():
            serializer._validated_data.update({'subjects_taught' : subjects_taught})
            serializer._validated_data.update({'learning_center_levels': levels})
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        form = CustomLearningCenterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return Response(status=status.HTTP_200_OK)


class SearchLearningCenter(APIView, ABC):
    serializer_class = LearningCenterInfoSerializer
    def get(self, request):
        name = request.query_params.get('name', '')
        level_name = request.query_params.get('level', '').split(',')
        subjects_taught = request.query_params.get('subjects_taught', '').split(',')
        lat = request.query_params.get('lat', '')
        lon = request.query_params.get('lon', '')
        dis = request.query_params.get('dis', '')

        response = []
        result_learning_centers = self.search_learning_centers(name, level_name, subjects_taught)
        if (lat and lon and dis):
            if (dis > 20):
                dis = 20
            elif (dis < 0):
                dis = 0
            result_learning_centers = self.search_by_distance(result_learning_centers, lat, lon, dis)
        for lc in result_learning_centers:
            serializer = self.serializer_class(lc)
            response.append(serializer.data)

        return Response(response, status=status.HTTP_200_OK)

    def search_learning_centers(self, name='', level_name=[], subjects_taught=[]):
        query = Q(status='approve')

        if name:
            query &= Q(name__icontains=name)

        for level in level_name:
            query &= Q()
        # queryset = LearningCenter.objects.select_related().filter(query).order_by('-popularity')
        queryset = LearningCenter.objects.select_related().filter(query)
            
        return queryset

    def search_by_distance(self, center_list, user_latitude, user_longtitude, dis):
        print(type(center_list))

        dis = float(dis) if dis.isnumeric() else 0
        learning_centers = self.filter_learning_centers_in_distance(user_latitude, user_longtitude, dis)
        if not learning_centers:
            return Response({"message": f"No Learning Centers found within {dis}km dis."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LearningCenterInfoSerializer(learning_centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_learning_centers_in_distance(self, lat, lon, max_distance_km=5):
        learning_centers = LearningCenter.objects.all()
        filtered_centers = []

        user_location = (lat, lon)
        for center in learning_centers:
            lc_location = center.location
            center_location = (lc_location.latitude, lc_location.longitude)
            dis = self.vector_distance(*user_location, *center_location)

            if dis <= max_distance_km:
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

        dis = earth_radius * c

        return dis

class LearningCenterDefaultPendingPage(APIView):
    def get(self, request):
        if not request.user.has_perm('LearningCenter.learning_center_admin'):
            return Response(
                {'message': 'user doesn\'t have permission'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            result = LearningCenter.objects.filter(status='waiting').order_by('date_created')
            serializer = LearningCenterInfoSerializer(result, many=True)
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


class LearningCenterInteriorView(APIView):
    authentication_classes = (IsAuthenticated, )

    def patch(self, request):
        data = request.data
        lc_id = data.get('learning_center_id', None)
        upload_image = request.FILES.get('image', None)
        user = request.user
        if (
            lc_id is None or
            upload_image is None or 
            not upload_image.__dict__.get('content_type').startswith('image/')
            ):
            return Response(
                { 'message': 'Invalid data' },
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            lc_id = UUID(lc_id, version=4)
        except ValueError:
                return Response(
                    {'message': 'Invalid UUID'},
                    status=status.HTTP_400_BAD_REQUEST
                    )

        learning_center = get_object_or_404(
            LearningCenter,
            learning_center_id=lc_id
            )

        if user.user_id != learning_center.owner:
            return Response(
                { 'message': 'Permission denied' },
                status=status.HTTP_403_FORBIDDEN
                )

        image = Images(image_file=upload_image)
        interior = LearningCenterInteriors(
            image=image,
            learning_center=learning_center
        )
        image.save()
        interior.save()
        return Response(
            { 'message': 'success' },
            status=status.HTTP_201_CREATED
            )

    def delete(self, request):
        data = request.data
        image_id = data.get('image_id', None)
        lc_id = data.get('learning_center_id', None)
        user = request.user
        if image_id is None or lc_id is None:
            return Response(
                { 'message': 'Invalid data' },
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            image_id = UUID(image_id, version=4)
            lc_id = UUID(lc_id, version=4)
        except ValueError:
                return Response(
                    {'message': 'Invalid UUID'},
                    status=status.HTTP_400_BAD_REQUEST
                    )

        image = get_object_or_404(Images, image_id=image_id)
        learning_center_id = image.learning_center_id
        learning_center = get_object_or_404(
            LearningCenter,
            learning_center_id=learning_center_id
            )

        if (
            learning_center_id != lc_id or
            user.user_id != learning_center.owner
            ):
            return Response(
                { 'message': 'Permission denied' },
                status=status.HTTP_403_FORBIDDEN
                )

        image.delete()
        return Response({ 'message': 'success' }, status=status.HTTP_200_OK)
