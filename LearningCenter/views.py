import http
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Profiles.models import Profiles
from Profiles.serializers import ProfileSerializer
from .forms import CustomLearningCenterForm
from .models import LearningCenter, Student, Tutor, TutorImageForm, SubjectsTaught
from Images.models import Images
from .serializers import LearningCenterInfoSerializer, StudentSerializer, TutorSerializer
from abc import ABC
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from uuid import UUID


class Index(APIView):
    def get(self, request):
        tutors_data = []
        tutors = Tutor.objects.all()

        for tutor in tutors:
            tutor_data = TutorSerializer(tutor).data
            tutors_data.append(tutor_data)

        return '''render(request, 'view_images.html', {"tutors": tutors})'''


class ViewLearningCenterInformation(APIView):
    url_table = {
        'Math': 'math',
        'Chemistry': 'chemistry',
        'Biology': 'biology',
        'Thai language': 'thai',
        'Social studies': 'socials',
        'Foreign language': 'foreign',
        'Programming': 'programming',
        'Physics': 'physics'
    }

    def get(self, request, lcid):
        def add_thumbnails(learning_center_data):
            learning_center_data['subject_thumbnails'] = {}
            subjects = SubjectsTaught.objects.filter(learning_center=learning_center_data['learning_center_id'])
            if subjects is not None:
                for subject in subjects:
                    url = self.url_table.get(subject, 'default')
                    subject_thumbnail_url = f'https://github.com/Roshanen/muda/blob/main/subject_img/{url}.png'
                    learning_center_data['subject_thumbnails'][subject] = subject_thumbnail_url

        def get_tutor_profile(tutors_data):
            tutor_list = []
            for tutor in tutors_data:
                profile = Profiles.objects.get(profile_id=tutor['profile_id'])
                profile_json = ProfileSerializer(profile).data
                tutor_list.append(profile_json)
            return tutor_list
        try:
            lcid = UUID(lcid, version=4)
        except ValueError:
            return Response({'message': 'Invalid Learning Center ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        learning_center = get_object_or_404(LearningCenter, learning_center_id=lcid)
        learning_center_json = LearningCenterInfoSerializer(learning_center).data
        add_thumbnails(learning_center_json)

        tutors = Tutor.objects.filter(learning_center=lcid).values()
        tutor_in_learning_center = get_tutor_profile(tutors)
        learning_center_json.update({'tutors': tutor_in_learning_center})

        return Response(learning_center_json, status=status.HTTP_200_OK)


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
        student_obj = Student.objects.filter(learning_center=lcid)
        student_list = []
        for student in student_obj:
            student_json = StudentSerializer(student).data
            profile = Profiles.objects.filter(profile_id=student_json['profile'])[0]
            profile_json = ProfileSerializer(profile).data
            student_list.append(profile_json)
        return Response({"students": student_list}, status=status.HTTP_200_OK)


class ViewTutors(APIView):
    def get(self, request, lcid):
        tutor_obj = Tutor.objects.filter(learning_center=lcid)
        tutor_list = []
        for tutor in tutor_obj:
            tutor_json = TutorSerializer(tutor).data
            profile = Profiles.objects.filter(profile_id=tutor_json['profile'])[0]
            profile_json = ProfileSerializer(profile).data
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
        serializer = LearningCenterInfoSerializer(data=request.data)
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
        serializer = LearningCenterInfoSerializer(result_learning_centers, many=True)

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
    
    def patch(self, request):
        data = request.data
        lc_id = data.get('learning_center_id', None)
        upload_image = request.FILES.get('image', None)
        if (lc_id is None or 
            upload_image is None or 
            not upload_image.__dict__.get('content_type').startswith('image/')
            ):
            return Response({ 'message': 'Invalid data' }, status=status.HTTP_400_BAD_REQUEST)
        image = Images(image_file=upload_image)
        image.save()
        return Response({ 'message': 'success' }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        image_id = data.get('image_id', None)
        if image_id is None:
            return Response({ 'message': 'Invalid data' }, status=status.HTTP_400_BAD_REQUEST)
        image = Images.objects.filter(image_id=image_id).first()
        image.delete()
        return Response({ 'message': 'success' }, status=status.HTTP_200_OK)