from accounts.models import User
from accounts.actions.verify_email import send_verification_email


def resend_verification_email(email: str) -> None:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return

    if user.is_verified:
        return

    send_verification_email(user)