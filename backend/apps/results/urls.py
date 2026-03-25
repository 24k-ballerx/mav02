from django.urls import path
from . import views
from .views import ResultUploadView # Added this import for ResultUploadView

urlpatterns = [
    path('', views.ResultListView.as_view(), name='result-list'),
    path('upload/', ResultUploadView.as_view(), name='result-upload'), # Added this path
    path('<int:pk>/', views.ResultDetailView.as_view(), name='result-detail'),
]
