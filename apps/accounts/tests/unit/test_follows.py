import pytest
from accounts.models import User, Follow
from accounts.actions.follows import follow_user, unfollow_user, accept_follow, reject_follow


@pytest.mark.django_db
class TestFollowActions:
    def setup_method(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='password123'
        )

    def test_follow_user_success(self):
        follow = follow_user(follower=self.user1, followee=self.user2)
        assert follow.follower == self.user1
        assert follow.followee == self.user2
        assert follow.status == Follow.Status.ACCEPTED

    def test_cannot_follow_yourself(self):
        with pytest.raises(ValueError, match='cannot follow yourself'):
            follow_user(follower=self.user1, followee=self.user1)

    def test_cannot_follow_twice(self):
        follow_user(follower=self.user1, followee=self.user2)
        with pytest.raises(ValueError, match='already following'):
            follow_user(follower=self.user1, followee=self.user2)

    def test_unfollow_success(self):
        follow_user(follower=self.user1, followee=self.user2)
        unfollow_user(follower=self.user1, followee=self.user2)
        assert not Follow.objects.filter(follower=self.user1, followee=self.user2).exists()

    def test_unfollow_not_following(self):
        with pytest.raises(ValueError, match='not following'):
            unfollow_user(follower=self.user1, followee=self.user2)

    def test_accept_follow_success(self):
        follow = Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.PENDING
        )
        accepted = accept_follow(follow_id=follow.id, user=self.user2)
        assert accepted.status == Follow.Status.ACCEPTED

    def test_accept_follow_wrong_user(self):
        follow = Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.PENDING
        )
        with pytest.raises(ValueError, match='cannot accept'):
            accept_follow(follow_id=follow.id, user=self.user1)

    def test_reject_follow_success(self):
        follow = Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.PENDING
        )
        reject_follow(follow_id=follow.id, user=self.user2)
        assert not Follow.objects.filter(id=follow.id).exists()

    def test_reject_follow_wrong_user(self):
        follow = Follow.objects.create(
            follower=self.user1,
            followee=self.user2,
            status=Follow.Status.PENDING
        )
        with pytest.raises(ValueError, match='cannot reject'):
            reject_follow(follow_id=follow.id, user=self.user1)