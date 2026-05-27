import pytest
from unittest.mock import patch
from accounts.models import User, PasswordResetToken
from accounts.actions.password_reset import request_password_reset, confirm_password_reset


@pytest.mark.django_db
class TestPasswordResetAction:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='oldpassword123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_reset_request_nonexistent_email_does_nothing(self):
        request_password_reset(email='nonexistent@example.com')

    def test_reset_request_creates_token(self):
        with patch('accounts.actions.password_reset.send_mail'):
            request_password_reset(email='test@example.com')
        assert PasswordResetToken.objects.filter(user=self.user).exists()

    def test_confirm_reset_changes_password(self):
        token = PasswordResetToken.objects.create(user=self.user)
        confirm_password_reset(token=str(token.token), new_password='newpassword123')
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword123')

    def test_confirm_reset_marks_token_as_used(self):
        token = PasswordResetToken.objects.create(user=self.user)
        confirm_password_reset(token=str(token.token), new_password='newpassword123')
        token.refresh_from_db()
        assert token.is_used is True

    def test_invalid_token_raises_error(self):
        with pytest.raises(ValueError, match='Invalid token'):
            confirm_password_reset(
                token='00000000-0000-0000-0000-000000000000',
                new_password='newpassword123'
            )

    def test_expired_token_raises_error(self):
        from django.utils import timezone
        from datetime import timedelta
        token = PasswordResetToken.objects.create(user=self.user)
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        with pytest.raises(ValueError, match='expired or already been used'):
            confirm_password_reset(token=str(token.token), new_password='newpassword123')