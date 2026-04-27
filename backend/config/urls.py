"""
Root URL configuration for Maverick International School Portal.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/auth/', include('apps.accounts.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/results/', include('apps.results.urls')),
    path('api/notices/', include('apps.notices.urls')),
    path('api/timetable/', include('apps.timetable.urls')),

    # Root & Index
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('index.html', TemplateView.as_view(template_name='index.html')),

    # Frontend Pages
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('students.html', TemplateView.as_view(template_name='students.html'), name='students'),
    path('courses.html', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('results.html', TemplateView.as_view(template_name='results.html'), name='results'),
    path('timetable.html', TemplateView.as_view(template_name='timetable.html'), name='timetable'),
    path('notices.html', TemplateView.as_view(template_name='notices.html'), name='notices'),
    path('profile.html', TemplateView.as_view(template_name='profile.html'), name='profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
