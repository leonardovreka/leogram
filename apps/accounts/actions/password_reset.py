from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User, PasswordResetToken


def request_password_reset(email: str) -> None:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return

    PasswordResetToken.objects.filter(user=user, is_used=False).delete()

    token = PasswordResetToken.objects.create(user=user)

    reset_link = f"http://localhost:8000/api/auth/password/reset-confirm?token={token.token}"

    send_mail(
        subject='Reset your LeoGram password',
        message=f'Hi {user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nThis link expires in 24 hours.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def confirm_password_reset(token: str, new_password: str) -> None:
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        raise ValueError('Invalid token')

    if not reset_token.is_valid():
        raise ValueError('Token has expired or already been used')

    reset_token.is_used = True
    reset_token.save()

    user = reset_token.user
    user.set_password(new_password)
    user.save()