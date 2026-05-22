import pytest
from accounts.models import User
from accounts.actions.login import login_user


@pytest.mark.django_db
class TestLoginAction:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='testemail@example.com',
            username='testuser',
            password='password123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_login_with_email_returns_tokens(self):
        tokens = login_user(email_or_username='testemail@example.com', password='password123')
        assert 'access' in tokens
        assert 'refresh' in tokens

    def test_login_with_username_returns_tokens(self):
        tokens = login_user(email_or_username='testuser', password='password123')
        assert 'access' in tokens
        assert 'refresh' in tokens

    def test_wrong_password_raises_error(self):
        with pytest.raises(ValueError, match='Invalid credentials'):
            login_user(email_or_username='testemail@example.com', password='wrongpassword')

    def test_nonexistent_user_raises_error(self):
        with pytest.raises(ValueError, match='Invalid credentials'):
            login_user(email_or_username='nobodyemail@example.com', password='password123')

    def test_unverified_user_raises_error(self):
        self.user.is_verified = False
        self.user.save()
        with pytest.raises(ValueError, match='verify your email'):
            login_user(email_or_username='testemail@example.com', password='password123')