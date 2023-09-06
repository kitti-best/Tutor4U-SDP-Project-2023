from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.EmailRegistrationAPIViews.as_view()), 
    path('sign-in', views.EmailLoginAPIViews.as_view())
]