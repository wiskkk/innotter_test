from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UpdateUserSerializer, UserSerializer)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class PermissionMixin(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'update':  # put
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action == 'retrieve':
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action == 'list':
            permission_classes = (permissions.AllowAny,)
        elif self.action == 'create':  # post
            permission_classes = (permissions.AllowAny,)
        elif self.action == 'partial_update':  # patch
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        return [permission() for permission in permission_classes]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(PermissionMixin):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UpdateUserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UpdateUserSerializer(user)
        return Response(serializer.data)
