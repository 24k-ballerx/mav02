"""
Root URL configuration for Maverick International School Portal.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/auth/', include('apps.accounts.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/results/', include('apps.results.urls')),
    path('api/notices/', include('apps.notices.urls')),
    path('api/timetable/', include('apps.timetable.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
