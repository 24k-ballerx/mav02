from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'term', 'academic_year', 'ca_score', 'exam_score', 'total_score', 'grade')
    list_filter = ('term', 'academic_year', 'course')
    search_fields = ('student__email', 'student__student_id', 'course__code', 'course__title')
    readonly_fields = ('total_score', 'grade')
    
    fieldsets = (
        ('Student & Course', {
            'fields': ('student', 'course')
        }),
        ('Academic Details', {
            'fields': ('term', 'academic_year')
        }),
        ('Scores', {
            'fields': ('ca_score', 'exam_score', 'total_score', 'grade')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
    )
