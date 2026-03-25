from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.results.models import Result
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample results'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding results...')
        
        # Get or create a student
        student, created = User.objects.get_or_create(
            email='student@maverick.edu.ng',
            defaults={
                'first_name': 'Chukwuemeka',
                'last_name': 'Obi',
                'role': User.Role.STUDENT,
                'student_id': 'STD001',
                'class_name': 'SS 3A'
            }
        )
        if created:
            student.set_password('student123')
            student.save()

        # Get all courses
        courses = Course.objects.all()
        if not courses.exists():
            self.stdout.write(self.style.ERROR('No courses found. Please run seed_courses first.'))
            return

        academic_year = '2025/2026'
        term = Result.Term.THIRD

        for course in courses:
            # Random scores
            ca = random.randint(20, 30)
            exam = random.randint(40, 70)
            
            Result.objects.update_or_create(
                student=student,
                course=course,
                term=term,
                academic_year=academic_year,
                defaults={
                    'ca_score': ca,
                    'exam_score': exam,
                    'remarks': 'Excellent performance.' if (ca+exam) > 80 else 'Good work.'
                }
            )
            self.stdout.write(f'Added result for {course.code}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded results.'))
