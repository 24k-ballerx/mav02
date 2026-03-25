from rest_framework import serializers
from .models import Result
from apps.accounts.serializers import UserProfileSerializer
from apps.courses.serializers import CourseSerializer

class ResultSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    total_score = serializers.ReadOnlyField()
    grade = serializers.ReadOnlyField()

    class Meta:
        model = Result
        fields = [
            'id', 'student', 'course', 'term', 'academic_year',
            'ca_score', 'exam_score', 'total_score', 'grade',
            'remarks', 'created_at', 'updated_at'
        ]
