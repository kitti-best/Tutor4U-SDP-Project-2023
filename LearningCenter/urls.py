from django.urls import path
from LearningCenter import views

urlpatterns = [
    path('create/', views.CreateLearningCenter.as_view(), name='create-learning-center'),
    path('change-status/<str:name>/<str:status>/', views.ChangeLearningCenterStatus.as_view(), name='change-learning-center-status'),
    path('delete/<id>/', views.DeleteLearningCenter.as_view(), name='delete-learning-center'),
    path('edit/<id>/', views.EditLearningCenter.as_view(), name='edit-learning-center'),
    path('search/', views.SearchLearningCenter.as_view(), name='search-learning-center'),
    path("view/<id>/", views.ViewLearningCenterInformation.as_view(), name="view-learning-center"),
    
    path('manage-location/create/<str:learning_center_name>/', views.ManageLocation.as_view(), name='create-location'),
    path('manage-location/edit/<str:learning_center_name>/', views.ManageLocation.as_view(), name='edit-location'),
    path('manage-location/delete/<str:learning_center_name>/', views.ManageLocation.as_view(), name='delete-location'),
]