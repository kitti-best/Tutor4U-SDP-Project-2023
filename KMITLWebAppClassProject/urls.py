from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from KMITLWebAppClassProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('/', include("LearningCenter.urls")),
    path('learning_center/', include("LearningCenter.urls")),
    path('learning_center_admin/', include("LearningCenterAdmin.urls")),
    path('master_admin/', include("MasterAdmin.urls")),
    path('user/', include("User.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
