import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestRegisterAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = '/api/auth/register'

    def test_register_success(self):
        payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post(self.url, payload, format='json')

        assert response.status_code == 201
        assert response.data['email'] == 'test@example.com'
        assert response.data['username'] == 'testuser'
        assert 'password' not in response.data

    def test_register_duplicate_email(self):
        payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.client.post(self.url, payload, format='json')

        payload['username'] = 'testuser2'
        response = self.client.post(self.url, payload, format='json')

        assert response.status_code == 400

    def test_register_missing_fields(self):
        payload = {'email': 'testemail@example.com'}

        response = self.client.post(self.url, payload, format='json')

        assert response.status_code == 400

    def test_register_invalid_email(self):
        payload = {
            'email': 'notemail',
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post(self.url, payload, format='json')

        assert response.status_code == 400

    def test_register_short_password(self):
        payload = {
            'email': 'testemail@example.com',
            'username': 'testuser',
            'password': '123'
        }

        response = self.client.post(self.url, payload, format='json')

        assert response.status_code == 400