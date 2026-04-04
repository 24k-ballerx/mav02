from django.core.management.base import BaseCommand
from apps.timetable.models import TimetableEntry
from apps.courses.models import Course
import random

class Command(BaseCommand):
    help = 'Seeds Nigerian curriculum timetable data'

    def handle(self, *args, **kwargs):
        TimetableEntry.objects.all().delete()
        
        courses = list(Course.objects.all())
        if not courses:
            self.stdout.write(self.style.ERROR('No courses found! Run seed_courses first.'))
            return

        target_classes_jss = ['JSS 1A', 'JSS 1B', 'JSS 2A', 'JSS 2B', 'JSS 3A', 'JSS 3B']
        target_classes_ss = ['SS 1A', 'SS 1B', 'SS 2A', 'SS 2B', 'SS 3A', 'SS 3B']
        
        # Course split
        jss_courses = [c for c in courses if '101' in c.code]
        ss_courses = [c for c in courses if '201' in c.code]

        # Nigerian School Period Structure (40 mins each)
        jss_periods = [
            (1, '08:30:00', '09:10:00'),
            (2, '09:10:00', '09:50:00'),
            (3, '09:50:00', '10:30:00'),
            # 10:30 - 10:50: Short Break
            (4, '10:50:00', '11:30:00'),
            (5, '11:30:00', '12:10:00'),
            (6, '12:10:00', '12:50:00'),
            # 12:50 - 01:30: Long Break
            (7, '13:30:00', '14:10:00'),
            (8, '14:10:00', '14:50:00'),
        ]

        ss_periods = jss_periods + [
            (9, '14:50:00', '15:30:00'),
            (10, '15:30:00', '16:10:00'),
        ]
        
        entries_created = 0
        for target_class in target_classes_jss + target_classes_ss:
            is_jss = target_class.startswith('JSS')
            class_courses = jss_courses if is_jss else ss_courses
            class_periods = jss_periods if is_jss else ss_periods
            
            for day in range(5):  # 0=Mon, 4=Fri
                used_courses = []
                for period_num, start_time, end_time in class_periods:
                    # Avoid duplicate courses in the same day if possible
                    available = [c for c in class_courses if c not in used_courses]
                    course = random.choice(available if available else class_courses)
                    used_courses.append(course)
                    
                    room = f"Room {random.randint(1, 15)}"
                    if course.department in ['Science', 'Physics', 'Chemistry', 'Biology']:
                        room = f"Lab {random.choice(['A', 'B', 'C'])}"
                    elif course.department == 'Mathematics':
                        room = "Room 12"
                    
                    TimetableEntry.objects.create(
                        course=course,
                        target_class=target_class,
                        day_of_week=day,
                        period=period_num,
                        start_time=start_time,
                        end_time=end_time,
                        room=room
                    )
                    entries_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {entries_created} timetable entries for JSS and SS.'))
