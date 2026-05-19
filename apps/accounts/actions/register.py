from accounts.models import User


def register_user(email: str, username: str, password: str) -> User:
    if User.objects.filter(email=email).exists():
        raise ValueError('A user with this email already exists')

    if User.objects.filter(username=username).exists():
        raise ValueError('A user with this username already exists')

    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
    )

    return user