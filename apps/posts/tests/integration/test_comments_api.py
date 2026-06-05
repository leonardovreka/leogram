import pytest
from rest_framework.test import APIClient
from accounts.models import User
from posts.models import Post, Comment


@pytest.mark.django_db
class TestCommentsAPI:
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
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )

    def test_add_comment_success(self):
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments',
            {'content': 'Great post!'},
            format='json'
        )
        assert response.status_code == 201
        assert response.data['content'] == 'Great post!'

    def test_list_comments(self):
        Comment.objects.create(post=self.post, author=self.user, content='First comment')
        Comment.objects.create(post=self.post, author=self.user, content='Second comment')
        response = self.client.get(f'/api/posts/{self.post.id}/comments')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_delete_own_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='My comment'
        )
        response = self.client.delete(f'/api/comments/{comment.id}')
        assert response.status_code == 200

    def test_delete_other_users_comment(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='password123'
        )
        comment = Comment.objects.create(
            post=self.post,
            author=other_user,
            content='Other comment'
        )
        response = self.client.delete(f'/api/comments/{comment.id}')
        assert response.status_code == 400

    def test_add_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments',
            {'content': 'Great post!'},
            format='json'
        )
        assert response.status_code == 401