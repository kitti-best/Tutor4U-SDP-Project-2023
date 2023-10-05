from rest_framework import serializers

from Locations.serializers import LocationsSerializer
from .models import LearningCenter, Tutor, Student, Locations, Subjects, LearningCenterLevels, SubjectsTaught, Levels

class LearningCenterInfoSerializer(serializers.ModelSerializer):
    location = LocationsSerializer()

    class Meta:
        model = LearningCenter
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        learning_center_levels_data = validated_data.pop('learning_center_levels', [])
        subjects_taught_data = validated_data.pop('subjects_taught', [])

        location = Locations.objects.create(**location_data)
        learning_center = LearningCenter.objects.create(location=location, **validated_data)

        for subject_data in subjects_taught_data:
            subject_name = subject_data['subject']
            subject = Subjects.objects.get(subject_name=subject_name)
            SubjectsTaught.objects.create(learning_center=learning_center, subject=subject)

        for level_data in learning_center_levels_data:
            level_name = level_data['level']
            level = Levels.objects.get(level_name=level_name)
            LearningCenterLevels.objects.create(learning_center=learning_center, level=level)

        return learning_center

    def data(self, learning_center):
        data = super().data
        
        tutors = learning_center.tutor_set.all()
        students = learning_center.student_set.all()
        thumbnail = learning_center.thumbnail.get_image_url()
        subjects_taught = learning_center.subjectstaught_set.all()
        
        self.get_subjects_taught(subjects_taught, data)
        data.update({'thumbnail': thumbnail})
        data.update({'tutors': self.get_profile(tutors)})
        data.update({'students': self.get_profile(students)})
        return data
    
    def get_profile(self, data):
        result = []
        for tutor in data:
            profile = tutor.profile
            result.append(profile.get_profile())
        return result
    
    def get_subjects_taught(self, subjects_data, response):
        subjects_taught_list = []
        for subject_taught in subjects_data:
            subject = subject_taught.subject
            subjects_taught_list.append(subject.get_subject())
        response.update({'subjects_taught': subjects_taught_list})
        return response


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
