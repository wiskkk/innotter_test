from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Page, Post, Tag
from .serializers import PageSerializer, PostSerializer, TagsSerializer


class PermissionMixin(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'update':  # put
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action == 'create':  # post
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action == 'partial_update':  # patch
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action == 'destroy':  # delete
            permission_classes = (permissions.IsAdminUser,)
        else:
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        return [permission() for permission in permission_classes]


class PageViewSet(PermissionMixin):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(owner_email=self.request.user.email)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
