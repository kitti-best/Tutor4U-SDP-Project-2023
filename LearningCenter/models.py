from django.db import models
from django.core.validators import MinLengthValidator
from User.models import UserModel
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
import uuid

class Location(models.Model):
    house_number = models.CharField(max_length=15, default='')
    section = models.CharField(max_length=10, default='')
    street = models.CharField(max_length=15, default='')
    sub_district = models.CharField(max_length=30, default='')
    district = models.CharField(max_length=30, default='')
    province = models.CharField(max_length=30, default='')
    country = models.CharField(max_length=30, default="Thailand")

    class Meta:
        verbose_name_plural = "Locations"

class LearningCenter(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    profile_picture_url = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    latitude = models.FloatField(max_length=15, default=0)
    longtitude = models.FloatField(max_length=15, default=0)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=30, default='', validators=[RegexValidator(regex="((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))")])
    email = models.EmailField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # The user who owns the learning center
    subjects_taught = ArrayField(models.CharField(max_length=255, blank=False))
    levels = ArrayField(models.CharField(max_length=255, blank=False))
    popularity = models.FloatField(max_length=15, default=0)
    LC_STATUS = (
        ('waiting', 'waiting'),
        ('approve', 'approve'),
        ('reject', 'reject')
    )
    status = models.CharField(max_length=20,choices=LC_STATUS, editable=False, default='waiting')

    def __str__(self):
        return(f"{self.name}")

    def update_status(self, status):
        self.status = status
    
    class Meta:
        permissions = [('approvable', 'can approve or reject the learning center')]
