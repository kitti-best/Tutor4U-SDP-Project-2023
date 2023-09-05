from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.EmailRegistrationAPIViews.as_view())
]