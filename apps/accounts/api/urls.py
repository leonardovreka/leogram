from django.urls import path
from .views import (
    RegisterView,
    ConfirmEmailView,
    ResendVerificationView,
    LoginView,
    TokenRefreshView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('email/confirm', ConfirmEmailView.as_view(), name='confirm_email'),
    path('email/resend', ResendVerificationView.as_view(), name='resend_verification'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('password/reset-request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset-confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]