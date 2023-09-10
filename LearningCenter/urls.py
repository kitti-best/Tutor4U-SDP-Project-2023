from django.urls import path
from . import views

urlpatterns = [
    path("view/<id>", views.ViewLearningCenterInformation.as_view(), name="view"),
]
