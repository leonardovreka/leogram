from posts.models import Post
from posts.actions.image import validate_and_upload_image


def create_post(author, title: str, image_file) -> Post:
    image_url = validate_and_upload_image(image_file)

    post = Post.objects.create(
        author=author,
        title=title,
        image_url=image_url,
    )

    return post