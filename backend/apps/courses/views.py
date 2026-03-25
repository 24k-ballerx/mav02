from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    from rest_framework import filters
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'code', 'department']

    def get_queryset(self):
        queryset = super().get_queryset()
        dept = self.request.query_params.get('department')
        if dept:
            queryset = queryset.filter(department__iexact=dept)
        return queryset

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
