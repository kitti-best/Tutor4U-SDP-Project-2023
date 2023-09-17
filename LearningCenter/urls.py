from django.urls import path
from .views import ManageLearningCenter
from . import views

urlpatterns = [
    path('learningcenters/', views.ManageLearningCenter.as_view(), name='manage-learning-center'),
    path('search/', views.SearchLearningCenter.as_view(), name='search-learning-center'),
    path('change-status/<str:name>/<str:status>/', views.ChangeLearningCenterStatus.as_view()),
    path("view/<id>", views.ViewLearningCenterInformation.as_view(), name="view"),
]
