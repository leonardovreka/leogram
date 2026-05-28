from accounts.models import User, Follow


def follow_user(follower: User, followee: User) -> Follow:
    if follower == followee:
        raise ValueError('You cannot follow yourself')

    if Follow.objects.filter(follower=follower, followee=followee).exists():
        raise ValueError('You are already following this user')

    follow = Follow.objects.create(
        follower=follower,
        followee=followee,
        status=Follow.Status.ACCEPTED,
    )

    return follow


def unfollow_user(follower: User, followee: User) -> None:
    try:
        follow = Follow.objects.get(follower=follower, followee=followee)
        follow.delete()
    except Follow.DoesNotExist:
        raise ValueError('You are not following this user')


def accept_follow(follow_id: int, user: User) -> Follow:
    try:
        follow = Follow.objects.get(id=follow_id)
    except Follow.DoesNotExist:
        raise ValueError('Follow request not found')

    if follow.followee != user:
        raise ValueError('You cannot accept this follow request')

    if follow.status != Follow.Status.PENDING:
        raise ValueError('This follow request is not pending')

    follow.status = Follow.Status.ACCEPTED
    follow.save()
    return follow


def reject_follow(follow_id: int, user: User) -> None:
    try:
        follow = Follow.objects.get(id=follow_id)
    except Follow.DoesNotExist:
        raise ValueError('Follow request not found')

    if follow.followee != user:
        raise ValueError('You cannot reject this follow request')

    follow.delete()