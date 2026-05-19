import pytest
from accounts.actions.register import register_user


@pytest.mark.django_db
class TestRegisterAction:
    def test_creates_user_successfully(self):
        email = 'testemail@example.com'
        username = 'testuser'
        password = 'testpassword123'

        user = register_user(email=email, username=username, password=password)

        assert user.id is not None
        assert user.email == email
        assert user.username == username
        assert user.is_verified is False

    def test_password_is_hashed(self):
        user = register_user(
            email='testemail@example.com',
            username='testuser',
            password='testpassword123'
        )

        assert user.password != 'testpassword123'

    def test_duplicate_email_raises_error(self):
        register_user('testemail@example.com', 'testuser1', 'password123')

        with pytest.raises(ValueError, match='email already exists'):
            register_user('testemail@example.com', 'testuser2', 'password123')

    def test_duplicate_username_raises_error(self):
        register_user('testemail1@example.com', 'testuser', 'password123')

        with pytest.raises(ValueError, match='username already exists'):
            register_user('testemail2@example.com', 'testuser', 'password123')