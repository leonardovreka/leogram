from django.urls import path
from .views import CreatePostView, FeedView, PostDetailView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('posts/feed', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),
]