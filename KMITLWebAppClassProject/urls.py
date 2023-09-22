from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('feed/', include("LearningCenter.urls")),
    path('learning_center/', include("LearningCenter.urls")),
    path('learning_center_admin/', include("LearningCenterAdmin.urls")),
    path('master_admin/', include("MasterAdmin.urls")),
    path('user/', include("User.urls")),
    path('auth/', include("authentication.urls")),
]
