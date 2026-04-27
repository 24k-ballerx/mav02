from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.notices.models import Notice

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample notices'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding notices...')
        
        # Get or create an admin user as author
        admin = User.objects.filter(role=User.Role.ADMIN).first()
        if not admin:
            self.stdout.write(self.style.ERROR('No Admin user found. Please run seed_users first.'))
            return

        sample_notices = [
            {
                'title': 'Third Term Examination Schedule',
                'content': 'The third term examinations will commence on July 15th, 2026. Please ensure all project works are submitted by July 10th.',
                'category': Notice.Category.ACADEMIC,
                'audience': Notice.Audience.EVERYONE,
                'is_urgent': True
            },
            {
                'title': 'Annual Inter-House Sports Competition',
                'content': 'We are excited to announce our annual inter-house sports day on May 20th. Parents are cordially invited to attend.',
                'category': Notice.Category.EVENT,
                'audience': Notice.Audience.EVERYONE,
                'is_urgent': False
            },
            {
                'title': 'School Fee Payment Deadline',
                'content': 'This is a reminder that the deadline for third term school fee payment is May 5th. Please visit the bursary for clarifications.',
                'category': Notice.Category.FINANCE,
                'audience': Notice.Audience.PARENTS,
                'is_urgent': True
            },
            {
                'title': 'Staff Meeting: Curriculum Review',
                'content': 'There will be a mandatory staff meeting this Friday at 3:00 PM in the Main Hall to discuss the new curriculum updates.',
                'category': Notice.Category.ACADEMIC,
                'audience': Notice.Audience.TEACHERS,
                'is_urgent': False
            }
        ]

        for n in sample_notices:
            Notice.objects.get_or_create(
                title=n['title'],
                defaults={
                    'content': n['content'],
                    'category': n['category'],
                    'audience': n['audience'],
                    'is_urgent': n['is_urgent'],
                    'author': admin
                }
            )
            self.stdout.write(f'Added notice: {n["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded notices.'))
