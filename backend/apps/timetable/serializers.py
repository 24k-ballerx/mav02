from rest_framework import serializers
from .models import TimetableEntry
from apps.courses.serializers import CourseSerializer

class TimetableEntrySerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = TimetableEntry
        fields = ['id', 'course', 'course_details', 'target_class', 'day_of_week', 'day_name', 'period', 'start_time', 'end_time', 'room']
