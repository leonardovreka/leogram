import pytest
from accounts.models import User
from posts.models import Post, Comment
from posts.actions.comments import add_comment, delete_comment


@pytest.mark.django_db
class TestCommentActions:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            image_url='http://minio:9000/leogram/posts/test.jpg'
        )

    def test_add_comment_success(self):
        comment = add_comment(author=self.user, post_id=self.post.id, content='Great post!')
        assert comment.id is not None
        assert comment.content == 'Great post!'
        assert comment.author == self.user
        assert comment.post == self.post

    def test_add_comment_nonexistent_post(self):
        with pytest.raises(ValueError, match='Post not found'):
            add_comment(author=self.user, post_id=9999, content='Great post!')

    def test_delete_comment_success(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Great post!'
        )
        delete_comment(comment_id=comment.id, user=self.user)
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_delete_comment_wrong_user(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='password123'
        )
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Great post!'
        )
        with pytest.raises(ValueError, match='only delete your own comments'):
            delete_comment(comment_id=comment.id, user=other_user)

    def test_delete_nonexistent_comment(self):
        with pytest.raises(ValueError, match='Comment not found'):
            delete_comment(comment_id=9999, user=self.user)