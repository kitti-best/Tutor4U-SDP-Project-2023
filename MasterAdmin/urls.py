from django.urls import path

from . import views

urlpatterns = [
    path("add-admin/", views.AddAdmin.as_view()),
]