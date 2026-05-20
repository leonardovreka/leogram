from django.urls import path
from .views import RegisterView, ConfirmEmailView, ResendVerificationView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('email/confirm', ConfirmEmailView.as_view(), name='confirm_email'),
    path('email/resend', ResendVerificationView.as_view(), name='resend_verification'),
]