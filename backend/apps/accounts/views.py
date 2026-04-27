"""
Authentication views for Maverick International School Portal.
"""
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
)

from apps.courses.models import Course
from apps.results.models import Result
from apps.notices.models import Notice

User = get_user_model()


# ─── Login ───────────────────────────────────────────────────────────────────

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Body: { "email": "...", "password": "..." }
    Returns: { "access": "...", "refresh": "...", "user": {...} }
    """
    permission_classes = [AllowAny]


# ─── Logout ──────────────────────────────────────────────────────────────────

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Body: { "refresh": "<refresh_token>" }
    Blacklists the refresh token so it cannot be reused.
    Requires: Bearer access token in Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {'detail': 'Invalid or already blacklisted token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK
        )


# ─── Token Refresh ────────────────────────────────────────────────────────────

class TokenRefreshView(APIView):
    """
    POST /api/auth/token/refresh/
    Body: { "refresh": "<refresh_token>" }
    Returns: { "access": "<new_access_token>", "refresh": "<new_refresh_token>" }
    No authorization header needed.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            data = {
                'access':  str(token.access_token),
                'refresh': str(token),  # rotated refresh token
            }
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data, status=status.HTTP_200_OK)


# ─── Current User ─────────────────────────────────────────────────────────────

class MeView(APIView):
    """
    GET /api/auth/me/
    Returns the authenticated user's profile.
    Useful for the frontend to restore session on page reload.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)


# ─── Change Password ──────────────────────────────────────────────────────────

class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Body: { "current_password": "...", "new_password": "...", "confirm_password": "..." }
    Requires: Bearer access token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'detail': 'Password changed successfully. Please log in again.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Forgot Password ──────────────────────────────────────────────────────────

class ForgotPasswordView(APIView):
    """
    POST /api/auth/forgot-password/
    Body: { "email": "..." }
    Sends a password-reset email (if the email exists).
    Always returns 200 to prevent email enumeration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        # Always return success — don't reveal whether email exists
        return Response(
            {'detail': 'If that email is registered, a reset link has been sent.'},
            status=status.HTTP_200_OK
        )


# ─── Reset Password ───────────────────────────────────────────────────────────

class ResetPasswordView(APIView):
    """
    POST /api/auth/reset-password/
    Body: { "token": "...", "new_password": "...", "confirm_password": "..." }
    Validates the one-time token (30 min expiry) and sets the new password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'detail': 'Password reset successful. You can now log in.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(APIView):
    """
    GET /api/auth/stats/
    Returns global stats for the dashboard cards.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = {
            'total_students': User.objects.filter(role=User.Role.STUDENT).count(),
            'total_teachers': User.objects.filter(role=User.Role.TEACHER).count(),
            'total_courses': Course.objects.count(),
            'total_notices': Notice.objects.count(),
            'urgent_notices': Notice.objects.filter(is_urgent=True).count(),
            'recent_results': Result.objects.count(), # Just a count for now
        }
        return Response(stats)
