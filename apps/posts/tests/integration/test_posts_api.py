import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User, Follow
from posts.models import Post


@pytest.mark.django_db
class TestPostsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )
        self.user.is_verified = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_post_success(self):
        image = SimpleUploadedFile(
            'test.jpg',
            b'fake image content',
            content_type='image/jpeg'
        )

        with patch('posts.actions.create_post.validate_and_upload_image') as mock_upload:
            mock_upload.return_value = 'http://minio:9000/leogram/posts/test.jpg'
            response = self.client.post(
                '/api/posts/',
                {'title': 'Test Post', 'image_file': image},
                format='multipart'
            )

        assert response.status_code == 201
        assert response.data['title'] == 'Test Post'

    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        image = SimpleUploadedFile('test.jpg', b'fake', content_type='image/jpeg')
        response = self.client.post(
            '/api/posts/',
            {'title': 'Test Post', 'image_file': image},
            format='multipart'
        )
        assert response.status_code == 401

    def test_get_post_detail(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )
        response = self.client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        assert response.data['title'] == 'Test Post'

    def test_delete_own_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )
        response = self.client.delete(f'/api/posts/{post.id}')
        assert response.status_code == 200

    def test_delete_other_users_post(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='password123'
        )
        post = Post.objects.create(
            author=other_user,
            title='Other Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )
        response = self.client.delete(f'/api/posts/{post.id}')
        assert response.status_code == 403

    def test_feed_shows_followed_users_posts(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='password123'
        )
        Follow.objects.create(
            follower=self.user,
            followee=other_user,
            status='accepted'
        )
        Post.objects.create(
            author=other_user,
            title='Other Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )
        response = self.client.get('/api/posts/feed')
        assert response.status_code == 200
        assert len(response.data) == 1