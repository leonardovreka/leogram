from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'image_url', 'author_username', 'created_at']
        read_only_fields = ['id', 'image_url', 'author_username', 'created_at']


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    image_file = serializers.ImageField()