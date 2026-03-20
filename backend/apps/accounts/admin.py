"""
Admin site configuration for the accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'get_full_name', 'role', 'class_name', 'is_active', 'date_joined')
    list_filter   = ('role', 'is_active', 'is_staff', 'gender')
    search_fields = ('email', 'first_name', 'last_name', 'student_id', 'staff_id')
    ordering      = ('-date_joined',)

    fieldsets = (
        ('Login',        {'fields': ('email', 'password')}),
        ('Personal',     {'fields': ('first_name', 'last_name', 'phone', 'gender', 'date_of_birth', 'address', 'avatar')}),
        ('Role & Class', {'fields': ('role', 'class_name', 'student_id', 'guardian_name', 'guardian_phone')}),
        ('Staff',        {'fields': ('staff_id', 'department', 'join_date')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display  = ('user', 'token', 'created_at', 'used')
    list_filter   = ('used',)
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')
