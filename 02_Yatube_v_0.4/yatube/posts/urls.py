from django.urls import path

from posts.views import (add_comment, follow_index, group_posts, index,
                         post_create, post_detail, post_edit, profile,
                         profile_follow, profile_unfollow)

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('group/<slug:slug>/', group_posts, name='group_list'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('follow/', follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        profile_unfollow,
        name='profile_unfollow'
    ),
]
