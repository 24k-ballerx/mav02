"""
URL configuration for the accounts app.
All routes are prefixed with /api/auth/ from config/urls.py
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView as JWTRefreshView

from .views import (
    LoginView,
    LogoutView,
    TokenRefreshView,
    MeView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    DashboardStatsView,
)

urlpatterns = [
    # Authentication
    path('login/',          LoginView.as_view(),          name='auth-login'),
    path('logout/',         LogoutView.as_view(),         name='auth-logout'),
    path('token/refresh/',  TokenRefreshView.as_view(),   name='auth-token-refresh'),

    # Logged-in user
    path('me/',             MeView.as_view(),             name='auth-me'),

    # Password management
    path('change-password/', ChangePasswordView.as_view(),  name='auth-change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(),  name='auth-forgot-password'),
    path('reset-password/',  ResetPasswordView.as_view(),   name='auth-reset-password'),

    # Dashboard Stats
    path('stats/',          DashboardStatsView.as_view(),  name='auth-stats'),
]
