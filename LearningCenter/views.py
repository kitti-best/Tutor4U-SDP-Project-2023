import http
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import CustomLearningCenterForm
from .models import LearningCenter, Student, Tutor, TutorImageForm
from .serializers import LearningCenterInfoSerializer, LearningCenterStudentsSerializer, LearningCenterTutorSerializer
from abc import ABC
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404


class Index(APIView):
    def get(self, request):
        tutors_data = []
        tutors = Tutor.objects.all()

        for tutor in tutors:
            tutor_data = LearningCenterTutorSerializer(tutor).data
            tutors_data.append(tutor_data)

        return render(request, 'view_images.html', {"tutors": tutors})


class ViewLearningCenterInformation(APIView):
    def get(self, request, lcid):
        # get LC object
        learning_center = get_object_or_404(LearningCenter, _uuid=lcid)
        # serialize it to be json
        learning_center_data = LearningCenterInfoSerializer(learning_center).data
        try:
            learning_center_data['subject_thumbnails'] = {}
            learning_center_subjects = learning_center_data.get['subjects_taught']
            for subject in learning_center_subjects:
                subject_thumbnail_url = f'https://github.com/Roshanen/muda/blob/main/subject_img/{subject}.png'
                learning_center_data['subject_thumbnails'][subject] = subject_thumbnail_url
        except KeyError:
            return Response(learning_center_data, status=status.HTTP_404_NOT_FOUND)

        # use LC id to get accord tutor
        learning_center_id = learning_center_data['_uuid']
        # get tutor object
        tutors = Tutor.objects.filter(learning_center=learning_center_id).values()
        # add tutors to response
        learning_center_data['tutors'] = tutors

        return Response(learning_center_data, status=status.HTTP_200_OK)


class ViewLearningCenterStudentInformation(APIView):
    def get(self, request, name):
        learning_center = get_object_or_404(LearningCenter, name=name)
        learning_center = LearningCenterInfoSerializer(learning_center)
        learning_center_student = LearningCenterStudentsSerializer(learning_center)
        return Response(learning_center_student.data, status=status.HTTP_200_OK)


class EditLearningCenter(APIView):
    # @login_required (use this if want to make user login first to access this also use: from django.contrib.auth.decorators import login_required)
    def edit_learning_center(request):
        if request.method == 'POST':
            form = CustomLearningCenterForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return Response(status=status.HTTP_200_OK)


class AddStudentToLearningCenter(APIView):
    def post(self, request):
        data: dict = request.data
        # django append _id for foreignkey column
        # So we will remove the old one and replace with ones with _id instead
        learning_center_id = data['learning_center']

        # learning_center = LearningCenter.objects.filter(_uuid=learning_center_id)
        # owner_id = learning_center.get()
        # if owner_id != request.user.id

        data['learning_center_id'] = learning_center_id

        # remove unwanted key
        data.pop('learning_center')
        data.pop('csrfmiddlewaretoken')

        # change query object to normal dictionary
        data_as_dict = {}
        # dict is mutable so this work
        [data_as_dict.update({key: val}) for key, val in data.items()]

        new_student = Student(**data_as_dict)
        new_student.save()
        return Response(status=status.HTTP_200_OK)


class AddTutorToLearningCenter(APIView):
    def post(self, request):
        data: dict = request.data
        print(data)
        # django append _id for foreignkey column
        # So we will remove the old one and replace with ones with _id instead
        learning_center_id = data['learning_center']
        user = request.user
        learning_center = LearningCenter(_uuid=learning_center_id)
        if user._uuid != learning_center.owner:
            return Response(status=http.HTTPStatus.UNAUTHORIZED)

        data['learning_center_id'] = learning_center_id

        # remove unwanted key
        data.pop('learning_center')
        data.pop('csrfmiddlewaretoken')

        # change query object to normal dictionary
        data_as_dict = {}
        # dict is mutable so this work
        [data_as_dict.update({key: val}) for key, val in data.items()]

        new_tutor = Tutor(**data_as_dict)
        new_tutor.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        form = TutorImageForm()
        return render(request, "gallery.html", {"form": form})


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
