from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.title}"