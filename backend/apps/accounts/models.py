"""
Custom User model for Maverick International School Portal.
Supports four roles: Admin, Teacher, Student, Parent.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager for the User model."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces Django's default User.
    Uses email as the primary identifier and adds a role field.
    """

    class Role(models.TextChoices):
        ADMIN   = 'admin',   'Administrator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'
        PARENT  = 'parent',  'Parent'

    # Core identity
    email      = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=64)
    last_name  = models.CharField(max_length=64)
    role       = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)

    # Extended profile
    phone       = models.CharField(max_length=20, blank=True)
    address     = models.TextField(blank=True)
    avatar      = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender      = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )

    # Staff-only fields
    staff_id    = models.CharField(max_length=20, blank=True)       # e.g. ADM001, TCH045
    department  = models.CharField(max_length=64, blank=True)
    join_date   = models.DateField(blank=True, null=True)

    # Student-only fields
    student_id  = models.CharField(max_length=20, blank=True)      # e.g. STU2023001
    class_name  = models.CharField(max_length=20, blank=True)      # e.g. SS 3A
    guardian_name  = models.CharField(max_length=128, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    # System fields
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login  = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email}) — {self.get_role_display()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def initials(self):
        f = self.first_name[0].upper() if self.first_name else ''
        l = self.last_name[0].upper() if self.last_name else ''
        return f + l

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT


class PasswordResetToken(models.Model):
    """One-time token for password reset emails."""
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token      = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used       = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.email}"

    def is_valid(self):
        """Token expires after 30 minutes."""
        from datetime import timedelta
        expiry = self.created_at + timedelta(minutes=30)
        return not self.used and timezone.now() < expiry
