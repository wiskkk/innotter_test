# from django.urls import path
#
# from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
#
# app_name = 'authentication'
#
# urlpatterns = [
#     path('user/', UserRetrieveUpdateAPIView.as_view()),
#     # path('users1/', UserView.as_view()),
#     # path('users1/<int:pk>', UserView.as_view({'get': 'retrieve'})),
#     path('users/', RegistrationAPIView.as_view()),
#     path('users/login/', LoginAPIView.as_view()),
# ]


from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView, RegisterView, UpdateProfileView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),

]
