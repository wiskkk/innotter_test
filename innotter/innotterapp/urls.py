from rest_framework.routers import DefaultRouter

from .views import PageViewSet, PostViewSet, TagViewSet

router = DefaultRouter()
router.register(r'page', PageViewSet, basename='page')
router.register(r'post', PostViewSet, basename='post')
router.register(r'tag', TagViewSet, basename='tag')
urlpatterns = router.urls
