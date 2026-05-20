import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from accounts.models import User, EmailVerificationToken


@pytest.mark.django_db
class TestConfirmEmailAPI:
    def setup_method(self):
        self.client = APIClient()
        self.confirm_url = '/api/auth/email/confirm'
        self.user = User.objects.create_user(
            email='testemail@example.com',
            username='testuser',
            password='password123'
        )
        self.token = EmailVerificationToken.objects.create(user=self.user)

    def test_valid_token_returns_200(self):
        payload = {'token': str(self.token.token)}

        response = self.client.post(self.confirm_url, payload, format='json')

        assert response.status_code == 200
        assert response.data['message'] == 'Email verified successfully'

    def test_invalid_token_returns_400(self):
        payload = {'token': '00000000-0000-0000-0000-000000000000'}

        response = self.client.post(self.confirm_url, payload, format='json')

        assert response.status_code == 400

    def test_malformed_token_returns_400(self):
        payload = {'token': 'notauuid'}

        response = self.client.post(self.confirm_url, payload, format='json')

        assert response.status_code == 400


@pytest.mark.django_db
class TestResendVerificationAPI:
    def setup_method(self):
        self.client = APIClient()
        self.resend_url = '/api/auth/email/resend'

    def test_resend_returns_200_always(self):
        payload = {'email': 'nonexistentemail@example.com'}

        response = self.client.post(self.resend_url, payload, format='json')

        assert response.status_code == 200

    def test_resend_invalid_email_returns_400(self):
        payload = {'email': 'notanemail'}

        response = self.client.post(self.resend_url, payload, format='json')

        assert response.status_code == 400