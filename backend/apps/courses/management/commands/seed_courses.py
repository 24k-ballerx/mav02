import random
from django.core.management.base import BaseCommand
from apps.courses.models import Course

class Command(BaseCommand):
    help = 'Seeds Nigerian curriculum courses'

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        
        jss_subjects = [
            ("MTH101", "Mathematics", "Mathematics"),
            ("ENG101", "English Language", "English"),
            ("BSC101", "Basic Science", "Science"),
            ("BTE101", "Basic Technology", "Science"),
            ("SST101", "Social Studies", "Arts"),
            ("CIV101", "Civic Education", "Arts"),
            ("CRS101", "C.R.S / I.R.S", "Arts"),
            ("PHE101", "Physical & Health Education", "Science"),
            ("BST101", "Business Studies", "Commerce"),
            ("AGR101", "Agricultural Science", "Science"),
            ("HEC101", "Home Economics", "Arts"),
            ("YOR101", "Local Language (Yoruba)", "Arts"),
            ("FRE101", "French", "Arts"),
            ("ICT101", "Computer Studies", "Computer Science"),
        ]
        
        ss_core = [
            ("MTH201", "Mathematics", "Mathematics"),
            ("ENG201", "English Language", "English"),
            ("CIV201", "Civic Education", "Arts"),
            ("DTP201", "Data Processing", "Computer Science"),
        ]
        
        ss_science = [
            ("BIO201", "Biology", "Biology"),
            ("CHM201", "Chemistry", "Chemistry"),
            ("PHY201", "Physics", "Physics"),
            ("FMT201", "Further Mathematics", "Mathematics"),
            ("GEO201", "Geography", "Science"),
        ]
        
        ss_arts = [
            ("LIT201", "Literature in English", "English"),
            ("GOV201", "Government", "Arts"),
            ("CRS201", "C.R.S / I.R.S", "Arts"),
            ("HIS201", "History", "History"),
        ]
        
        ss_commerce = [
            ("ECO201", "Economics", "Commerce"),
            ("ACC201", "Financial Accounting", "Commerce"),
            ("COM201", "Commerce", "Commerce"),
        ]

        all_courses = jss_subjects + ss_core + ss_science + ss_arts + ss_commerce
        
        for code, title, dept in all_courses:
            Course.objects.get_or_create(
                code=code,
                defaults={
                    "title": title,
                    "department": dept,
                    "description": f"{title} syllabus for Maverick International School."
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(all_courses)} Nigerian courses.'))
