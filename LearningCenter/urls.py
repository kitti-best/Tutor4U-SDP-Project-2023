from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    path("add_student", views.AddStudent.as_view(), name="add_student"),
    path("student/<lcid>", views.ViewStudents.as_view(), name="view_student"),
    path("tutor/<lcid>", views.ViewTutors.as_view(), name="view_tutor"),
    path("add_tutor", views.AddTutor.as_view(), name="add_tutor"),

    path("view/<lcid>", views.ViewLearningCenterInformation.as_view(), name="view"),
    path('manage/', views.ManageLearningCenter.as_view(), name='manage-learning-center'),

    path('change-status/', views.ChangeLearningCenterStatus.as_view()),
    path('pending-page/', views.LearningCenterDefaultPendingPage.as_view()),
    path('search/', views.SearchLearningCenter.as_view(), name='search-learning-center'),
    path('search/distance/', views.LearningCenterDistanceFilter.as_view(), name='search-learning-center'),
    path('interiors/', views.LearningCenterInteriorView.as_view(), name='learning-center-interior'),
]
