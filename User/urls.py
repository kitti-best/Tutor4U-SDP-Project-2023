from django.urls import path

from . import views

urlpatterns = [
  path('', views.UserAuthViewSet.as_view()),
  path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate')
]