from rest_framework import serializers
from Locations.serializers import LocationsSerializer
from .models import LearningCenter, Tutor, Student, Locations, Subjects, SubjectsTaught, Levels, LearningCenterLevels, LearningCenterInteriors



class SubjectsTaughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectsTaught
        fields = '__all__'

class LearningCenterInfoSerializer(serializers.ModelSerializer):
    location = LocationsSerializer()

    class Meta:
        model = LearningCenter
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        levels = validated_data.pop('learning_center_levels', [])
        subjects_taught = validated_data.pop('subjects_taught', [])
        
        location = Locations.objects.create(**location_data)
        learning_center = LearningCenter.objects.create(location=location, **validated_data)
        
        for subject_name in subjects_taught:
            subject = Subjects.objects.filter(subject_name=subject_name).first()
            if (subject):
                SubjectsTaught.objects.create(learning_center=learning_center, subject=subject)

        for level_name in levels:
            level = Levels.objects.filter(level_name=level_name).first()
            if (level):
                LearningCenterLevels.objects.create(learning_center=learning_center, level=level)
        
        return learning_center
    
    @property
    def data(self):
        data = super().data
        learning_center = self.instance
        
        thumbnail = learning_center.thumbnail.get_image_url()
        subjects_taught = learning_center.subjectstaught_set.all()
        levels = learning_center.learningcenterlevels_set.all()

        self.get_subjects_taught(subjects_taught, data)
        self.get_levels(levels, data)
        
        data.update({'thumbnail': thumbnail})
        
        return data
    
    def get_learning_center_detail(self, data):
        learning_center = self.instance
        tutors = learning_center.tutor_set.all()
        students = learning_center.student_set.all()
        interiors = learning_center.learningcenterinteriors_set.all()

        self.get_interiors(interiors, data)
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
        subject_thumbnails = []
        for subject_taught in subjects_data:
            subject = subject_taught.subject
            subjects_taught_list.append(subject.subject_name)
            subject_thumbnails.append(subject.image.get_image_url())
        
        response.update({'subjects_taught': subjects_taught_list})
        response.update({'subject_thumbnails': subject_thumbnails})
        return response
    
    def get_levels(self, levels_data, response):
        level_list = []
        for lc_level in levels_data:
            level = lc_level.level
            level_list.append(level.level_name)
        response.update({'levels': level_list})
        return level_list

    def get_interiors(self, interiors_data, response):
        interior_list = []
        for interior in interiors_data:
            image_url = interior.image.get_image_url() 
            interior_list.append(image_url)
        response.update({'interiors': interior_list})
        return interior_list
    
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

