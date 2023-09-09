from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import uuid

class LearningCenter(models.Model):
    _uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, unique=True)
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=150, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the learning center
    learning_sessions = models.ManyToManyField('TutoringSession', related_name='centers_hosting')
    population = models.IntegerField(max_length=255)

    def __str__(self):
        return(f"{self.name}")