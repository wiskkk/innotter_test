from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UpdateUserSerializer)
# from .models import User

from django.contrib.auth import get_user_model

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# class PermissionMixin(viewsets.ModelViewSet):
#
#     def get_permissions(self):
#         if self.action == 'update':  # put
#             permission_classes = (permissions.IsAdminUser,)
#         elif self.action == 'create':  # post
#             permission_classes = (permissions.AllowAny,)
#         elif self.action == 'partial_update':  # patch
#             permission_classes = (permissions.IsAdminUser,)
#         elif self.action == 'destroy':  # delete
#             permission_classes = (permissions.IsAdminUser,)
#         else:
#             permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#         return [permission() for permission in permission_classes]
#
#
# class UserProfileViewsSet(PermissionMixin):
#     serializer_class = UserProfileSerializer
#     queryset = User.objects.all()
#
#     def partial_update(self, request, *args, **kwargs):
#         instance = self.queryset.get(pk=kwargs.get('pk'))
#         serializer = self.serializer_class(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
