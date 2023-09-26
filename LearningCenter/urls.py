from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    path("add_student", views.AddStudentToLearningCenter.as_view(), name="add_student"),
    path("add_tutor", views.AddTutorToLearningCenter.as_view(), name="add_tutor"),

    path("view/<name>", views.ViewLearningCenterInformation.as_view(), name="view"),
    path('create/', views.ManageLearningCenter.as_view(), name='manage-learning-center'),

    path('change-status/', views.ChangeLearningCenterStatus.as_view()),
    path('pending-page/', views.LearningCenterDefaultPendingPage.as_view()),
    path('search/', views.SearchLearningCenter.as_view(), name='search-learning-center'),
]
