from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from innotterapp.views import (FollowUnfollowViewSet, LikeUnlikeViewSet,
                               PageViewSet, PostViewSet, RepliesViewSet,
                               TagViewSet, NewsView)

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'replies', RepliesViewSet, basename='reply')
router.register(r'likes', LikeUnlikeViewSet, basename='like')
router.register(r'follows', FollowUnfollowViewSet, basename='like')
# urlpatterns = router.urls
urlpatterns = [
    path('news/', NewsView.as_view({'get': 'list'}), name="news"),
    path('', include(router.urls)),
]
