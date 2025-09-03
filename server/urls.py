from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    path('subjects/', include('subjects.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
    path('dashboard/', include("dashboard.urls")),
    path('', include('users.urls')),
    
]
