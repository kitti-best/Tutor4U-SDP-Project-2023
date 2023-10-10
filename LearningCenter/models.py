from django.db import models
from django import forms
from User.models import UserModel
from django.core.validators import RegexValidator, MinLengthValidator
from Locations.models import Locations
from Images.models import Images, get_default_image
from Profiles.models import Profiles
import uuid

default_image = get_default_image


class LearningCenter(models.Model):
    learning_center_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        validators=[MinLengthValidator(4)], 
        max_length=150, 
        unique=True
        )
    description = models.TextField()
    website = models.URLField(blank=True,  default='', null=True)
    phone = models.CharField(
        max_length=30, 
        default='', 
        validators=[RegexValidator(
            regex="((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))"
            )]
        )
    email = models.EmailField(blank=True, default='', null=True)
    rating = models.FloatField(max_length=15, default=0)
    popularity = None
    
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)  # The user who owns the learning center
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True)
    thumbnail = models.ForeignKey(
        Images, 
        default=default_image, 
        on_delete=models.SET_DEFAULT
        )
    
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
        permissions = [
            ('learning_center_admin', 
            'can approve or reject the learning center, can view the waiting and reject learning center')]


class LearningCenterInteriors(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Images, default=default_image, on_delete=models.CASCADE)


class Student(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    
    def delete(self):
        self.profile.delete()
        super(Student, self).delete()


class Tutor(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    
    def delete(self):
        self.profile.delete()
        super(Tutor, self).delete()


class Subjects(models.Model):
    SUBJECT_CHOICES = (
        ("Biology", "Biology"),
        ("Chemistry", "Chemistry"),
        ("Foreign language", "Foreign language"),
        ("Math", "Math"),
        ("Physics", "Physics"),
        ("Programming", "Programming"),
        ("Science", "Science"),
        ("Social studies", "Social studies"),
        ("Thai language", "Thai language"),
    )
    subject_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    subject_name = models.CharField(
        max_length=20, 
        choices=SUBJECT_CHOICES, 
        editable=False, 
        null=False)
    image = models.ForeignKey(Images, default=default_image, on_delete=models.SET_DEFAULT)
    
    def get_subject(self):
        result = {
            'subject_name': self.subject_name,
            'image': self.image.get_image_url()
        }
        return result

class SubjectsTaught(models.Model):
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)


class Levels(models.Model):
    LEVEL_CHOICES = (
        ("University", "University"),
        ("Postgraduate", "Postgraduate"),
        ("Middle School", "Middle School"),
        ("Kindergarten", "Kindergarten"),
        ("Elementary", "Elementary"),
    )
    level_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    level_name = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES, 
        editable=False, 
        null=False
        )
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
