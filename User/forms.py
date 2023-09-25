from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile


class CustomUserForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = '__all__' # ('username', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'zipcode')
