from django.core.management.base import BaseCommand
from apps.courses.models import Course
from apps.timetable.models import TimetableEntry
import datetime

class Command(BaseCommand):
    help = 'Seed the database with sample timetable entries'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding timetable...')
        
        # Get some courses
        math = Course.objects.filter(code='MTH101').first()
        eng = Course.objects.filter(code='ENG101').first()
        csc = Course.objects.filter(code='ICT101').first()
        phy = Course.objects.filter(code='PHY201').first()

        if not math or not eng:
            self.stdout.write(self.style.ERROR('Courses not found. Please run seed_courses first.'))
            return

        target_class = 'SS 3A'
        
        # Clear existing for this class to avoid unique_together errors
        TimetableEntry.objects.filter(target_class=target_class).delete()

        entries = [
            # Monday
            {'course': math, 'day': 0, 'period': 1, 'start': '08:00', 'end': '08:40', 'room': 'Lab 1'},
            {'course': eng, 'day': 0, 'period': 2, 'start': '08:40', 'end': '09:20', 'room': 'Room 12'},
            {'course': csc, 'day': 0, 'period': 3, 'start': '09:20', 'end': '10:00', 'room': 'ICT Center'},
            # Tuesday
            {'course': phy, 'day': 1, 'period': 1, 'start': '08:00', 'end': '08:40', 'room': 'Physics Lab'},
            {'course': math, 'day': 1, 'period': 2, 'start': '08:40', 'end': '09:20', 'room': 'Lab 1'},
            # Wednesday
            {'course': eng, 'day': 2, 'period': 1, 'start': '08:00', 'end': '08:40', 'room': 'Room 12'},
            {'course': math, 'day': 2, 'period': 4, 'start': '10:50', 'end': '11:30', 'room': 'Lab 1'},
        ]

        for e in entries:
            TimetableEntry.objects.create(
                course=e['course'],
                target_class=target_class,
                day_of_week=e['day'],
                period=e['period'],
                start_time=e['start'],
                end_time=e['end'],
                room=e['room']
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded timetable for {target_class}.'))
