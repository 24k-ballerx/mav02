from rest_framework import generics, permissions
from .models import TimetableEntry
from .serializers import TimetableEntrySerializer

class TimetableListView(generics.ListAPIView):
    """
    GET /api/timetable/ - List all timetable entries, optionally filtered by `target_class`
    """
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = TimetableEntry.objects.all().select_related('course', 'course__teacher')
        
        target_class = self.request.query_params.get('target_class')
        if target_class:
            queryset = queryset.filter(target_class__iexact=target_class)
            
        day = self.request.query_params.get('day')
        if day is not None:
            queryset = queryset.filter(day_of_week=day)
            
        return queryset
