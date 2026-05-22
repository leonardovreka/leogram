from django.urls import path
from .views import (
    RegisterView,
    ConfirmEmailView,
    ResendVerificationView,
    LoginView,
    TokenRefreshView,
    LogoutView,
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('email/confirm', ConfirmEmailView.as_view(), name='confirm_email'),
    path('email/resend', ResendVerificationView.as_view(), name='resend_verification'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
]