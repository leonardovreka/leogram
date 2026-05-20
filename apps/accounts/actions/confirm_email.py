from accounts.models import EmailVerificationToken


def confirm_email(token: str):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        raise ValueError('Invalid token')

    if not verification_token.is_valid():
        raise ValueError('Token has expired or already been used')

    verification_token.is_used = True
    verification_token.save()

    user = verification_token.user
    user.is_verified = True
    user.save()

    return user