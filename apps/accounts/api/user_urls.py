from django.urls import path
from .views import (
    FollowView,
    UnfollowView,
    AcceptFollowView,
    RejectFollowView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('users/<str:username>/follow', FollowView.as_view(), name='follow'),
    path('users/<str:username>/unfollow', UnfollowView.as_view(), name='unfollow'),
    path('follows/<int:pk>/accept', AcceptFollowView.as_view(), name='accept_follow'),
    path('follows/<int:pk>/reject', RejectFollowView.as_view(), name='reject_follow'),
    path('users/<str:username>/followers', FollowersListView.as_view(), name='followers'),
    path('users/<str:username>/following', FollowingListView.as_view(), name='following'),
]