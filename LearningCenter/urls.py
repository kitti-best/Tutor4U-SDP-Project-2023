from django.urls import path
from .views import ManageLearningCenter
from . import views

urlpatterns = [
    path('learningcenters/', views.ManageLearningCenter.as_view(), name='manage-learning-center'),
    path('search/', views.SearchLearningCenter.as_view(), name='search-learning-center'),
    path('change-status/', views.ChangeLearningCenterStatus.as_view()),
    path('pending-page/', views.LearningCenterDefaultPendingPage.as_view())
]
