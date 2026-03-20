"""
Management command to create demo/seed users for development.
Run with: python manage.py seed_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

DEMO_USERS = [
    {
        'email':      'admin@maverick.edu.ng',
        'password':   'admin123',
        'first_name': 'Emmanuel',
        'last_name':  'Okafor',
        'role':       'admin',
        'staff_id':   'ADM001',
        'department': 'Administration',
        'is_staff':   True,
        'is_superuser': True,
        'phone':      '+234 803 456 7890',
        'gender':     'male',
    },
    {
        'email':      'teacher@maverick.edu.ng',
        'password':   'teacher123',
        'first_name': 'Ngozi',
        'last_name':  'Adeleke',
        'role':       'teacher',
        'staff_id':   'TCH012',
        'department': 'English Language',
        'phone':      '+234 805 111 2222',
        'gender':     'female',
    },
    {
        'email':      'student@maverick.edu.ng',
        'password':   'student123',
        'first_name': 'Chukwuemeka',
        'last_name':  'Nwosu',
        'role':       'student',
        'student_id': 'STU2023001',
        'class_name': 'SS 3A',
        'guardian_name': 'Mr. Peter Nwosu',
        'guardian_phone': '+234 808 999 0001',
        'phone':      '+234 808 999 0002',
        'gender':     'male',
    },
    {
        'email':      'parent@maverick.edu.ng',
        'password':   'parent123',
        'first_name': 'Folake',
        'last_name':  'Balogun',
        'role':       'parent',
        'phone':      '+234 807 333 4444',
        'gender':     'female',
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo users for development.'

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for data in DEMO_USERS:
            email = data['email']
            password = data.pop('password')

            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'  SKIP  {email} (already exists)'))
                skipped += 1
                continue

            user = User.objects.create_user(password=password, **data)
            self.stdout.write(self.style.SUCCESS(f'  OK    {email} ({user.get_role_display()})'))
            created += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done! Created {created} users. Skipped {skipped}.'))
        self.stdout.write('')
        self.stdout.write('Demo credentials:')
        self.stdout.write('  admin@maverick.edu.ng   /  admin123')
        self.stdout.write('  teacher@maverick.edu.ng /  teacher123')
        self.stdout.write('  student@maverick.edu.ng /  student123')
        self.stdout.write('  parent@maverick.edu.ng  /  parent123')
