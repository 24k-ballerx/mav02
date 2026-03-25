from django.db import models
from django.conf import settings
from apps.courses.models import Course

class Result(models.Model):
    class Term(models.TextChoices):
        FIRST = 'first', 'First Term'
        SECOND = 'second', 'Second Term'
        THIRD = 'third', 'Third Term'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='results'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='results'
    )
    term = models.CharField(
        max_length=10, 
        choices=Term.choices, 
        default=Term.THIRD
    )
    academic_year = models.CharField(
        max_length=15, 
        default='2025/2026'
    )
    
    ca_score = models.PositiveSmallIntegerField(default=0)
    exam_score = models.PositiveSmallIntegerField(default=0)
    
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_score(self):
        return self.ca_score + self.exam_score

    @property
    def grade(self):
        total = self.total_score
        if total >= 75: return 'A1'
        if total >= 70: return 'B2'
        if total >= 65: return 'B3'
        if total >= 60: return 'C4'
        if total >= 55: return 'C5'
        if total >= 50: return 'C6'
        if total >= 45: return 'D7'
        if total >= 40: return 'E8'
        return 'F9'

    class Meta:
        unique_together = ('student', 'course', 'term', 'academic_year')
        ordering = ['student', 'course']

    def __str__(self):
        return f"{self.student.email} - {self.course.code} ({self.term})"
