import pytest
from rest_framework.test import APIClient
from accounts.models import User


@pytest.mark.django_db
class TestLoginAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = '/api/auth/login'
        self.user = User.objects.create_user(
            email='testemail@example.com',
            username='testuser',
            password='password123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_login_success_returns_tokens(self):
        payload = {'email_or_username': 'testemail@example.com', 'password': 'password123'}
        response = self.client.post(self.url, payload, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_with_username(self):
        payload = {'email_or_username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.url, payload, format='json')
        assert response.status_code == 200

    def test_login_wrong_password(self):
        payload = {'email_or_username': 'testemail@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.url, payload, format='json')
        assert response.status_code == 400

    def test_login_unverified_user(self):
        self.user.is_verified = False
        self.user.save()
        payload = {'email_or_username': 'testemail@example.com', 'password': 'password123'}
        response = self.client.post(self.url, payload, format='json')
        assert response.status_code == 400
        assert 'verify' in response.data['error'].lower()

    def test_logout_success(self):
        payload = {'email_or_username': 'testemail@example.com', 'password': 'password123'}
        login_response = self.client.post(self.url, payload, format='json')
        refresh_token = login_response.data['refresh']

        logout_response = self.client.post('/api/auth/logout', {'refresh': refresh_token}, format='json')
        assert logout_response.status_code == 200

    def test_refresh_token(self):
        payload = {'email_or_username': 'testemail@example.com', 'password': 'password123'}
        login_response = self.client.post(self.url, payload, format='json')
        refresh_token = login_response.data['refresh']

        refresh_response = self.client.post('/api/auth/token/refresh', {'refresh': refresh_token}, format='json')
        assert refresh_response.status_code == 200
        assert 'access' in refresh_response.data