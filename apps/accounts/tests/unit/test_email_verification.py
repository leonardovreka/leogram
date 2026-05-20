import pytest
from unittest.mock import patch
from accounts.models import User, EmailVerificationToken
from accounts.actions.confirm_email import confirm_email
from accounts.actions.resend_verification import resend_verification_email


@pytest.mark.django_db
class TestConfirmEmailAction:
    def setup_method(self):
        with patch('accounts.actions.verify_email.send_mail'):
            from accounts.actions.register import register_user
            self.user = register_user(
                email='testemail@example.com',
                username='testuser',
                password='password123'
            )

    def test_valid_token_verifies_user(self):
        token = EmailVerificationToken.objects.get(user=self.user)

        confirm_email(token=str(token.token))

        self.user.refresh_from_db()
        assert self.user.is_verified is True

    def test_token_marked_as_used(self):
        token = EmailVerificationToken.objects.get(user=self.user)

        confirm_email(token=str(token.token))

        token.refresh_from_db()
        assert token.is_used is True

    def test_invalid_token_raises_error(self):
        with pytest.raises(ValueError, match='Invalid token'):
            confirm_email(token='00000000-0000-0000-0000-000000000000')

    def test_already_used_token_raises_error(self):
        token = EmailVerificationToken.objects.get(user=self.user)
        confirm_email(token=str(token.token))

        with pytest.raises(ValueError, match='expired or already been used'):
            confirm_email(token=str(token.token))

    def test_expired_token_raises_error(self):
        from django.utils import timezone
        from datetime import timedelta
        token = EmailVerificationToken.objects.get(user=self.user)
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()

        with pytest.raises(ValueError, match='expired or already been used'):
            confirm_email(token=str(token.token))


@pytest.mark.django_db
class TestResendVerificationAction:
    def test_nonexistent_email_does_nothing(self):
        resend_verification_email(email='nonexistentemail@example.com')

    def test_already_verified_user_does_nothing(self):
        user = User.objects.create_user(
            email='verifiedemail@example.com',
            username='verifieduser',
            password='password123'
        )
        user.is_verified = True
        user.save()

        with patch('accounts.actions.resend_verification.send_verification_email') as mock_send:
            resend_verification_email(email='verifiedemail@example.com')
            mock_send.assert_not_called()