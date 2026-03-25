from django.core.management.base import BaseCommand
from apps.timetable.models import TimetableEntry
from apps.courses.models import Course
import random

class Command(BaseCommand):
    help = 'Seeds initial timetable data'

    def handle(self, *args, **kwargs):
        TimetableEntry.objects.all().delete()
        
        courses = list(Course.objects.all())
        if not courses:
            self.stdout.write(self.style.ERROR('No courses found! Run seed_courses first.'))
            return

        target_classes_jss = ['JSS 1A', 'JSS 1B', 'JSS 2A', 'JSS 2B', 'JSS 3A', 'JSS 3B']
        target_classes_ss = ['SS 1A', 'SS 1B', 'SS 2A', 'SS 2B', 'SS 3A', 'SS 3B']
        
        # Determine JSS vs SS courses based on course code (101 for JSS, 201 for SS)
        jss_courses = [c for c in courses if '101' in c.code]
        ss_courses = [c for c in courses if '201' in c.code]

        if not jss_courses or not ss_courses:
            self.stdout.write(self.style.WARNING("Couldn't strictly split JSS/SS courses. Using all courses for all."))
            jss_courses = courses
            ss_courses = courses

        periods = [
            (1, '08:00:00', '08:40:00'),
            (2, '08:40:00', '09:20:00'),
            (3, '09:20:00', '10:00:00'),
            (4, '10:20:00', '11:00:00'),
            (5, '11:00:00', '11:40:00'),
            (6, '12:20:00', '13:00:00'),
            (7, '13:00:00', '13:40:00'),
        ]
        
        entries_created = 0
        for target_class in target_classes_jss + target_classes_ss:
            is_jss = target_class.startswith('JSS')
            class_courses = jss_courses if is_jss else ss_courses
            
            for day in range(5):  # 0=Mon, 4=Fri
                for period_num, start_time, end_time in periods:
                    course = random.choice(class_courses)
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {entries_created} timetable entries.'))
