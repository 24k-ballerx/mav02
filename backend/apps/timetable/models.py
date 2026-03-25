from django.db import models
from apps.courses.models import Course

class TimetableEntry(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_entries')
    target_class = models.CharField(max_length=50) # e.g., 'SS 3A'
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    period = models.IntegerField() # 1 to 7
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    class Meta:
        ordering = ['day_of_week', 'period']
        unique_together = ['target_class', 'day_of_week', 'period']

    def __str__(self):
        return f"{self.target_class} - {self.get_day_of_week_display()} p{self.period} - {self.course.code}"
