from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView, RegisterView, UserViewSet

app_name = 'authentication'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('', include(router.urls)),
]
