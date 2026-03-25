from rest_framework import generics, permissions, filters
from .models import Notice
from .serializers import NoticeSerializer

class NoticeListView(generics.ListCreateAPIView):
    """
    GET /api/notices/ - List notices based on audience
    POST /api/notices/ - Create notice (Admins/Teachers only)
    """
    serializer_class = NoticeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'is_urgent']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.BasePermission()] # Simple for now
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.all().select_related('author')
        
        # If student, show only 'everyone' and 'students'
        if not user.is_authenticated:
            return queryset.filter(audience='everyone')
            
        if user.role == 'student':
            return queryset.filter(audience__in=['everyone', 'students'])
        elif user.role == 'parent':
            return queryset.filter(audience__in=['everyone', 'parents'])
        
        # Admins and Teachers see everything
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/notices/{id}/
    UPDATE/DELETE /api/notices/{id}/ (Author or Admin only)
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)
