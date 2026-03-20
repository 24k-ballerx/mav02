from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.courses.models import Course

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial courses'

    def handle(self, *args, **kwargs):
        # Ensure we have a teacher
        teacher, created = User.objects.get_or_create(
            email='teacher@maverick.edu.ng',
            defaults={
                'first_name': 'Sarah',
                'last_name': 'Okonkwo',
                'role': 'teacher',
                'is_active': True,
            }
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('Created teacher user'))

        courses_data = [
            {
                'code': 'MTH101',
                'title': 'General Mathematics I',
                'description': 'Foundational mathematics including algebra and trigonometry.',
                'department': 'Mathematics',
                'teacher': teacher
            },
            {
                'code': 'ENG101',
                'title': 'English Composition',
                'description': 'Core English language and writing skills.',
                'department': 'English',
                'teacher': teacher
            },
            {
                'code': 'CSC201',
                'title': 'Introduction to Computer Science',
                'description': 'Basics of computing and programming.',
                'department': 'Computer Science',
                'teacher': teacher
            },
            {
                'code': 'PHY201',
                'title': 'General Physics I',
                'description': 'Mechanics and properties of matter.',
                'department': 'Physics',
                'teacher': teacher
            }
        ]

        for data in courses_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.code}'))
            else:
                self.stdout.write(self.style.WARNING(f'Course {course.code} already exists'))
