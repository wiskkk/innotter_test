from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from .views import (FollowView, PageViewSet,  # FollowUnfollowView, , LikeUnlikeView
                    PostViewSet, TagViewSet, RepliesViewSet, LikeUnlikeViewSet)

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'replies', RepliesViewSet, basename='reply')
router.register(r'likes', LikeUnlikeViewSet, basename='like')
# urlpatterns = router.urls
urlpatterns = [
    #     path('follow_unfollow/', FollowUnfollowView.as_view(), name="follow_unfollow"),
    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),
    # path('like/<int:pk>', LikeUnlikeView.as_view(), name='like_unlike'),
    path('', include(router.urls)),
]
