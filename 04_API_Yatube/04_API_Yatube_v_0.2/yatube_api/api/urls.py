from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register(r'follow', FollowViewSet, basename='follow')
router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'^posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
