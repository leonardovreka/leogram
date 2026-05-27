import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from accounts.models import User, PasswordResetToken


@pytest.mark.django_db
class TestPasswordResetAPI:
    def setup_method(self):
        self.client = APIClient()
        self.request_url = '/api/auth/password/reset-request'
        self.confirm_url = '/api/auth/password/reset-confirm'
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='oldpassword123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_reset_request_always_returns_200(self):
        payload = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.request_url, payload, format='json')
        assert response.status_code == 200

    def test_reset_request_existing_email_returns_200(self):
        with patch('accounts.actions.password_reset.send_mail'):
            payload = {'email': 'test@example.com'}
            response = self.client.post(self.request_url, payload, format='json')
        assert response.status_code == 200

    def test_reset_request_same_message_for_both(self):
        payload1 = {'email': 'nonexistent@example.com'}
        response1 = self.client.post(self.request_url, payload1, format='json')

        with patch('accounts.actions.password_reset.send_mail'):
            payload2 = {'email': 'test@example.com'}
            response2 = self.client.post(self.request_url, payload2, format='json')

        assert response1.data['message'] == response2.data['message']

    def test_confirm_reset_success(self):
        token = PasswordResetToken.objects.create(user=self.user)
        payload = {'token': str(token.token), 'new_password': 'newpassword123'}
        response = self.client.post(self.confirm_url, payload, format='json')
        assert response.status_code == 200

    def test_confirm_reset_invalid_token(self):
        payload = {'token': '00000000-0000-0000-0000-000000000000', 'new_password': 'newpassword123'}
        response = self.client.post(self.confirm_url, payload, format='json')
        assert response.status_code == 400

    def test_confirm_reset_short_password(self):
        token = PasswordResetToken.objects.create(user=self.user)
        payload = {'token': str(token.token), 'new_password': '123'}
        response = self.client.post(self.confirm_url, payload, format='json')
        assert response.status_code == 400