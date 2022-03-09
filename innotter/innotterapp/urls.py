from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from .views import PageViewSet, PostViewSet, TagViewSet, FollowView  # FollowUnfollowView,

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
# urlpatterns = router.urls
urlpatterns = [
    #     path('follow_unfollow/', FollowUnfollowView.as_view(), name="follow_unfollow"),
    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),
    path('', include(router.urls)),
]
