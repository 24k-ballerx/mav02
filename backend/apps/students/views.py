from django.db import models
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from apps.accounts.serializers import UserProfileSerializer

User = get_user_model()

class StudentListView(generics.ListAPIView):
    """
    GET /api/students/
    Returns a list of all users with role='student'.
    Supports simple search via query param ?search=
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(role=User.Role.STUDENT).order_by('last_name', 'first_name')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) | 
                models.Q(last_name__icontains=search) | 
                models.Q(student_id__icontains=search)
            )
        return queryset

class StudentDetailView(generics.RetrieveAPIView):
    """
    GET /api/students/{id}/
    Returns full profile of a specific student.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(role=User.Role.STUDENT)
