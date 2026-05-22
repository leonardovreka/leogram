from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


def login_user(email_or_username: str, password: str) -> dict:
    try:
        if '@' in email_or_username:
            user = User.objects.get(email=email_or_username)
        else:
            user = User.objects.get(username=email_or_username)
    except User.DoesNotExist:
        raise ValueError('Invalid credentials')

    if not user.check_password(password):
        raise ValueError('Invalid credentials')

    if not user.is_verified:
        raise ValueError('Please verify your email before logging in')

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }