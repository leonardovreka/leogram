import pytest
from rest_framework.test import APIClient
from accounts.models import User, Follow


@pytest.mark.django_db
class TestFollowAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='password123'
        )
        self.user1.is_verified = True
        self.user1.save()

        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='password123'
        )
        self.user2.is_verified = True
        self.user2.save()

        self.client.force_authenticate(user=self.user1)

    def test_follow_success(self):
        response = self.client.post(f'/api/users/user2/follow')
        assert response.status_code == 201

    def test_follow_nonexistent_user(self):
        response = self.client.post('/api/users/nobody/follow')
        assert response.status_code == 404

    def test_follow_yourself(self):
        response = self.client.post('/api/users/user1/follow')
        assert response.status_code == 400

    def test_unfollow_success(self):
        follow_user = Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.ACCEPTED
        )
        response = self.client.post('/api/users/user2/unfollow')
        assert response.status_code == 200

    def test_accept_follow_success(self):
        follow = Follow.objects.create(
            follower=self.user2,
            followee=self.user1,
            status=Follow.Status.PENDING
        )
        response = self.client.post(f'/api/follows/{follow.id}/accept')
        assert response.status_code == 200

    def test_reject_follow_success(self):
        follow = Follow.objects.create(
            follower=self.user2,
            followee=self.user1,
            status=Follow.Status.PENDING
        )
        response = self.client.post(f'/api/follows/{follow.id}/reject')
        assert response.status_code == 200

    def test_followers_list(self):
        Follow.objects.create(
            follower=self.user2,
            followee=self.user1,
            status=Follow.Status.ACCEPTED
        )
        response = self.client.get('/api/users/user1/followers')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_following_list(self):
        Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.ACCEPTED
        )
        response = self.client.get('/api/users/user1/following')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_unauthenticated_cannot_follow(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/users/user2/follow')
        assert response.status_code == 401