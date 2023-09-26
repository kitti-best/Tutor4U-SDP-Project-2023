from django import forms
from .models import LearningCenter

class CustomLearningCenterForm(forms.ModelForm):
    class Meta:
        model = LearningCenter
        fields = '__all__'
