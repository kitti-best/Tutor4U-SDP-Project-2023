from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.EmailRegistrationAPIViews.as_view()), 
    path('sign-in', views.LoginAPIViews.as_view()), 
    # path('sign-out', views.LogoutAPIViews.as_view()),
    path('token/refresh/', views.TokenRefreshAPIViews.as_view())
]