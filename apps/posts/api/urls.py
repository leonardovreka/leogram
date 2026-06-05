from django.urls import path
from .views import (
    CreatePostView,
    FeedView,
    PostDetailView,
    CommentsView,
    DeleteCommentView,
)

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('posts/feed', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comments', CommentsView.as_view(), name='comments'),
    path('comments/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
]