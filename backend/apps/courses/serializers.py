from rest_framework import serializers
from .models import Course
from apps.accounts.serializers import UserProfileSerializer

class CourseSerializer(serializers.ModelSerializer):
    teacher_details = UserProfileSerializer(source='teacher', read_only=True)
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'title', 'description', 'department', 
            'teacher', 'teacher_details', 'student_count', 
            'created_at', 'updated_at'
        ]
