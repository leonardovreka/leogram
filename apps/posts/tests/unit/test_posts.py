import pytest
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from posts.models import Post
from posts.actions.create_post import create_post


@pytest.mark.django_db
class TestCreatePostAction:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )

    def test_create_post_success(self):
        image = SimpleUploadedFile(
            'test.jpg',
            b'fake image content',
            content_type='image/jpeg'
        )

        with patch('posts.actions.create_post.validate_and_upload_image') as mock_upload:
            mock_upload.return_value = 'http://minio:9000/leogram/posts/test.jpg'
            post = create_post(author=self.user, title='Test Post', image_file=image)

        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.author == self.user
        assert post.image_url == 'http://minio:9000/leogram/posts/test.jpg'

    def test_create_post_invalid_image(self):
        image = SimpleUploadedFile(
            'test.jpg',
            b'fake image content',
            content_type='image/jpeg'
        )

        with patch('posts.actions.create_post.validate_and_upload_image') as mock_upload:
            mock_upload.side_effect = ValueError('Invalid image type')

            with pytest.raises(ValueError, match='Invalid image type'):
                create_post(author=self.user, title='Test Post', image_file=image)