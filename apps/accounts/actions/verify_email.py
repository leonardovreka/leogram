from django.core.mail import send_mail
from django.conf import settings
from accounts.models import EmailVerificationToken


def send_verification_email(user) -> None:
    # Delete any existing unused tokens for this user
    EmailVerificationToken.objects.filter(user=user, is_used=False).delete()

    # Create a new token
    token = EmailVerificationToken.objects.create(user=user)

    # Build the verification link
    verification_link = f"http://localhost:8000/api/auth/email/confirm?token={token.token}"

    send_mail(
        subject='Verify your LeoGram account',
        message=f'Hi {user.username},\n\nClick the link below to verify your account:\n\n{verification_link}\n\nThis link expires in 24 hours.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )