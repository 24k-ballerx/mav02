from django.db import models
from django.conf import settings

class Notice(models.Model):
    class Category(models.TextChoices):
        ACADEMIC = 'academic', 'Academic'
        URGENT = 'urgent', 'Urgent'
        EVENT = 'event', 'Event'
        FINANCE = 'finance', 'Finance'
        GENERAL = 'general', 'General'

    class Audience(models.TextChoices):
        EVERYONE = 'everyone', 'Everyone'
        STUDENTS = 'students', 'Students Only'
        PARENTS = 'parents', 'Parents Only'
        TEACHERS = 'teachers', 'Teachers Only'

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20, 
        choices=Category.choices, 
        default=Category.GENERAL
    )
    audience = models.CharField(
        max_length=20, 
        choices=Audience.choices, 
        default=Audience.EVERYONE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notices'
    )
    is_urgent = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_urgent', '-created_at']

    def __str__(self):
        return self.title
