import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.courses.models import Course
from apps.results.models import Result

def seed():
    students = User.objects.filter(role='student')
    courses = Course.objects.all()
    
    if not students.exists():
        print("No students found. Please seed users first.")
        return
    
    if not courses.exists():
        print("No courses found. Please seed courses first.")
        return

    terms = [Result.Term.FIRST, Result.Term.SECOND, Result.Term.THIRD]
    academic_year = '2025/2026'
    
    count = 0
    for student in students:
        # Give each student results for 5 random courses
        selected_courses = random.sample(list(courses), min(5, courses.count()))
        
        for course in selected_courses:
            for term in terms:
                ca = random.randint(15, 28)
                exam = random.randint(30, 68)
                
                result, created = Result.objects.update_or_create(
                    student=student,
                    course=course,
                    term=term,
                    academic_year=academic_year,
                    defaults={
                        'ca_score': ca,
                        'exam_score': exam,
                        'remarks': 'Good performance.' if ca + exam > 50 else 'Needs improvement.'
                    }
                )
                if created:
                    count += 1

    print(f"Successfully seeded {count} results.")

if __name__ == "__main__":
    seed()
