from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
import uuid

class LearningCenter(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    description = models.TextField()
    location = gis_models.PointField()
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True, null=True)
    phone_number = models.IntegerField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the learning center
    subjects_taught = models.CharField(max_length=255, blank=False)
    popularity = models.IntegerField(max_length=30, default=0)

    def __str__(self):
        return(f"{self.name}")
