from posts.models import Post, Comment


def add_comment(author, post_id: int, content: str) -> Comment:
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise ValueError('Post not found')

    comment = Comment.objects.create(
        post=post,
        author=author,
        content=content,
    )

    return comment


def delete_comment(comment_id: int, user) -> None:
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise ValueError('Comment not found')

    if comment.author != user:
        raise ValueError('You can only delete your own comments')

    comment.delete()