from rest_framework.routers import DefaultRouter

from .views import PageViewSet, PostViewSet, TagViewSet

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
urlpatterns = router.urls
