from django.contrib.auth.forms import UserChangeForm
from .models import UserModel


class CustomUserForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__' # ('username', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'zipcode')
