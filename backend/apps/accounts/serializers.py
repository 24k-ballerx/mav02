"""
Serializers for authentication endpoints.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PasswordResetToken

User = get_user_model()


# ─── JWT LOGIN ──────────────────────────────────────────────────────────────

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the default JWT serializer to include user profile
    data in the login response so the frontend can display it immediately.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Embed lightweight user info into the token payload
        token['email']     = user.email
        token['full_name'] = user.get_full_name()
        token['role']      = user.role
        token['initials']  = user.initials
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active:
            raise serializers.ValidationError('Your account has been deactivated. Contact admin.')

        # Append full user profile to the response
        data['user'] = UserProfileSerializer(user).data
        return data


# ─── USER PROFILE ────────────────────────────────────────────────────────────

class UserProfileSerializer(serializers.ModelSerializer):
    """Read-only profile snapshot returned on login and GET /profile/."""
    full_name = serializers.SerializerMethodField()
    initials  = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'gender', 'date_of_birth', 'address',
            'staff_id', 'student_id', 'class_name', 'department',
            'join_date', 'guardian_name', 'guardian_phone',
            'avatar_url', 'initials', 'date_joined', 'last_login',
        ]
        read_only_fields = fields

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_initials(self, obj):
        return obj.initials

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Writable serializer for profile updates (PUT /api/profile/)."""

    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'phone', 'gender',
            'date_of_birth', 'address',
        ]


# ─── CHANGE PASSWORD ─────────────────────────────────────────────────────────

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        validate_password(attrs['new_password'], self.context['request'].user)
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


# ─── FORGOT PASSWORD ──────────────────────────────────────────────────────────

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self._user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            # Return success either way to prevent email enumeration
            self._user = None
        return value

    def save(self):
        if not self._user:
            return  # Silently skip — don't reveal if email exists

        # Invalidate old tokens for this user
        PasswordResetToken.objects.filter(user=self._user, used=False).update(used=True)

        token_str = get_random_string(length=64)
        PasswordResetToken.objects.create(user=self._user, token=token_str)

        reset_url = f"{settings.FRONTEND_URL}/reset-password.html?token={token_str}"

        send_mail(
            subject='Maverick International — Password Reset',
            message=(
                f"Hello {self._user.get_full_name()},\n\n"
                f"Click the link below to reset your password (valid for 30 minutes):\n\n"
                f"{reset_url}\n\n"
                f"If you did not request this, you can safely ignore this email.\n\n"
                f"— Maverick International School Portal"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self._user.email],
            fail_silently=True,
        )


# ─── RESET PASSWORD ───────────────────────────────────────────────────────────

class ResetPasswordSerializer(serializers.Serializer):
    token            = serializers.CharField()
    new_password     = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            self._reset_token = PasswordResetToken.objects.select_related('user').get(token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError('Invalid or expired reset token.')

        if not self._reset_token.is_valid():
            raise serializers.ValidationError('This reset link has expired or already been used.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        validate_password(attrs['new_password'], self._reset_token.user)
        return attrs

    def save(self):
        user = self._reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])

        self._reset_token.used = True
        self._reset_token.save(update_fields=['used'])
        return user
