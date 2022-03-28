from django.contrib.auth import get_user_model
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UserSerializer)

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class PermissionMixin(viewsets.ModelViewSet):

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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ('^username',)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'put', 'patch', 'head']

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # def update(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UpdateUserSerializer(user)
    #     return Response(serializer.data)

    # def partial_update(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UpdateUserSerializer(user)
    #     return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
