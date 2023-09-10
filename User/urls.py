from django.urls import path

from . import views
from django.urls import path

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("profile/<username>", views.ViewSelfProfile.as_view(), name="view_profile"),
]
