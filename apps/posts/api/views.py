from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Comment
from posts.actions.create_post import create_post
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer, CreateCommentSerializer

from posts.actions.comments import add_comment, delete_comment


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = create_post(
                author=request.user,
                title=serializer.validated_data['title'],
                image_file=serializer.validated_data['image_file'],
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from accounts.models import Follow
        following_ids = Follow.objects.filter(
            follower=request.user,
            status='accepted'
        ).values_list('followee_id', flat=True)

        posts = Post.objects.filter(
            author_id__in=following_ids
        ).order_by('-created_at')

        return Response(PostSerializer(posts, many=True).data, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user:
            return Response({'error': 'You can only delete your own posts'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)

class CommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CreateCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = add_comment(
                author=request.user,
                post_id=pk,
                content=serializer.validated_data['content'],
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(post=post).order_by('created_at')
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            delete_comment(comment_id=pk, user=request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)