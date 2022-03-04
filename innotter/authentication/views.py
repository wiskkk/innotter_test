# from rest_framework import status, viewsets
# from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from .models import User
# from .serializers import (LoginSerializer, RegistrationSerializer,
#                           UserSerializer)
#
#
# class RegistrationAPIView(APIView):
#     """
#     Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)

#
# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def update(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# # class UserView(viewsets.ViewSet):
# #     """
# #     A simple ViewSet that for listing or retrieving users.
# #     """
#
# # def list(self, request):
# #     queryset = User.objects.all()
# #     serializer = UserSerializer(queryset, many=True)
# #     return Response(serializer.data)
#
# # def retrieve(self, request, pk=None):
# #     queryset = User.objects.all()
# #     user = get_object_or_404(queryset, pk=pk)
# #     serializer = UserSerializer(user)
# #     return Response(serializer.data)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, viewsets, permissions, status


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
