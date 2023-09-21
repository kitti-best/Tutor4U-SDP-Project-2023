from django.db import models
from django.core.validators import MinLengthValidator
from User.models import UserModel
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
import uuid

class LearningCenter(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    description = models.TextField()
    latitude = models.FloatField(max_length=15, default=0)
    longtitude = models.FloatField(max_length=15, default=0)
    house_number = models.CharField(max_length=15, default='') # เลขที่บ้าน
    section = models.CharField(max_length=10, default='') # หมู่บ้าน
    street = models.CharField(max_length=15, default='') # ถนน
    sub_district = models.CharField(max_length=30, default='') # ตำบล
    district = models.CharField(max_length=30, default='') # อำเภอ
    province = models.CharField(max_length=30, default='') # จังหวัด
    country = models.CharField(max_length=30, default="Thailand")
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=30, default='', validators=[RegexValidator(regex="((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))")])
    email = models.EmailField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # The user who owns the learning center
    subjects_taught = ArrayField(models.CharField(max_length=255, blank=False)) 
    popularity = models.IntegerField(default=0)
    LC_STATUS = (
        ('waiting', 'waiting'),
        ('approve', 'approve'),
        ('reject', 'reject')
    )
    status = models.CharField(max_length=20, choices=LC_STATUS, editable=False, default='waiting')

    def __str__(self):
        return(f"{self.name}")

    def update_status(self, status):
        self.status = status
    
    class Meta:
        permissions = [('learning_center_admin', 'can approve or reject the learning center, can view the waiting and reject learning center')]
