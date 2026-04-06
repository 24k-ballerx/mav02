import csv
from django.db.models import Prefetch
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Result
from .serializers import ResultSerializer
from apps.courses.models import Course
from apps.accounts.models import User

class ResultUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # ROLE SECURITY CHECK
        if request.user.role not in ['admin', 'teacher']:
            return Response(
                {"error": "Unauthorized. Only administrators and teachers can upload results."},
                status=status.HTTP_403_FORBIDDEN
            )

        file = request.FILES.get('file')
        target_class = request.data.get('class')
        subject_title = request.data.get('subject')
        term = request.data.get('term')

        if not file or not target_class or not subject_title or not term:
            return Response({"error": "Missing required fields or file."}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({"error": "Only CSV files are supported currently."}, status=status.HTTP_400_BAD_REQUEST)

        # Look up course
        course = Course.objects.filter(title__iexact=subject_title).first()
        if not course:
            return Response({"error": f"Course '{subject_title}' not found."}, status=status.HTTP_404_NOT_FOUND)

        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        # Expected columns: student_id, ca_score, exam_score
        processed = 0
        errors = []
        
        for row in reader:
            student_id = row.get('student_id')
            ca = row.get('ca_score', 0)
            exam = row.get('exam_score', 0)
            
            if not student_id:
                continue
                
            student = User.objects.filter(student_id__iexact=student_id).first()
            if not student:
                errors.append(f"Student ID {student_id} not found.")
                continue
                
            try:
                result, created = Result.objects.update_or_create(
                    student=student,
                    course=course,
                    academic_year='2025/2026', # Static for now, could be dynamic
                    term=term,
                    defaults={
                        'ca_score': float(ca),
                        'exam_score': float(exam)
                    }
                )
                processed += 1
            except Exception as e:
                errors.append(f"Error processing {student_id}: {str(e)}")

        return Response({
            "message": f"Successfully processed {processed} records.",
            "errors": errors
        }, status=status.HTTP_200_OK)

class ResultListView(generics.ListAPIView):
    """
    GET /api/results/
    Returns results. Students see their own; Admins/Teachers see all.
    """
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Result.objects.all().select_related('student', 'course')
        
        # Filter for students
        if user.role == 'student':
            queryset = queryset.filter(student=user)
        
        # Filtering by params
        student_id = self.request.query_params.get('student_id')
        course_id = self.request.query_params.get('course_id')
        term = self.request.query_params.get('term')
        academic_year = self.request.query_params.get('academic_year')
        search = self.request.query_params.get('search')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if term:
            queryset = queryset.filter(term__iexact=term)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
            
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__student_id__icontains=search)
            )
            
        return queryset

class ResultDetailView(generics.RetrieveAPIView):
    """
    GET /api/results/{id}/
    """
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Result.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Result.objects.filter(student=user)
        return Result.objects.all()
