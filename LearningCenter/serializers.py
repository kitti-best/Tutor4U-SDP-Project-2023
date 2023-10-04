from rest_framework import serializers
from .models import LearningCenter, Tutor, Student, Subjects

class LearningCenterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCenter
        fields = '__all__'


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
