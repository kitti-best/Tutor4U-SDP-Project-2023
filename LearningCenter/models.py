from django.db import models
from django import forms
from User.models import UserModel
from django.core.validators import RegexValidator, MinLengthValidator
from Locations.models import Locations
from Images.models import Images
from Profiles.models import Profiles
import uuid

default_image = Images.get_default_image()


class LearningCenter(models.Model):
    learning_center_id = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    description = models.TextField()
    website = models.URLField(blank=True,  default='', null=True)
    phone = models.CharField(
        max_length=30, 
        default='', 
        validators=[RegexValidator(regex="((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))")]
        )
    email = models.EmailField(blank=True, default='', null=True)
    popularity = models.FloatField(max_length=15, default=0)
    rating = models.FloatField(max_length=15, default=0)
    
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)  # The user who owns the learning center
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ForeignKey(Images, default=default_image, on_delete=models.SET_DEFAULT)
    
    LC_STATUS = (
        ('waiting', 'waiting'),
        ('approve', 'approve'),
        ('reject', 'reject')
    )
    status = models.CharField(max_length=20, choices=LC_STATUS, editable=False, default='waiting')
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    def update_status(self, status):
        self.status = status
    
    class Meta:
        order_with_respect_to = "learning_center_id"
        permissions = [('learning_center_admin', 'can approve or reject the learning center, can view the waiting and reject learning center')]


class LearningCenterInteriors(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Images, default=default_image, on_delete=models.CASCADE)


class Student(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)


class Tutor(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)


class Subjects(models.Model):
    subject_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    subject_name = models.CharField(max_length=255, default='')
    image = models.ForeignKey(Images, default=default_image, on_delete=models.SET_DEFAULT)


class SubjectsTaught(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)


class Levels(models.Model):
    level_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    level_name = models.CharField(max_length=255, null=False)
    image = models.ForeignKey(Images, default=default_image,on_delete=models.SET_DEFAULT)


class LearningCenterLevels(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE, null=True)


class TutorImageForm(forms.Form):
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()
    learning_center = forms.ModelChoiceField(
        queryset=LearningCenter.objects.all()
    )
