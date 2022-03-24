from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import PageFilterSet
from .models import Page, Post, Reply, Tag
from .producer import publish
from .serializers import (FollowerSerializer, PageSerializer,
                          PostLikeListSerializer, PostSerializer,
                          ReplySerializer, TagsSerializer)
from .tasks import send_plain_email, verify_email_identity

User = get_user_model()


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
    search_fields = ('^name', '=uuid')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = PageFilterSet

    def perform_create(self, serializer):
        verify_email_identity(email=self.request.user.email)
        serializer.save(owner=self.request.user)
        publish('page_created', serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('page_updated', serializer.data)

        return Response(serializer.data)


class PostViewSet(PermissionMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        email = (self.request.user.pages.first().followers.all())
        for i in email:
            send_plain_email.delay(owner=self.request.user.email, email=i.owner.email)
        serializer.save(page=self.request.user.pages.first())
        publish('post_created', serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('post_updated', serializer.data)

        return Response(serializer.data)


class RepliesViewSet(PermissionMixin):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class LikeUnlikeViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(like__username=self.request.user.username)
        return queryset

    @action(detail=True, methods=['post'])
    def liked(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.like.filter(pk=request.user.pk).exists():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        return Response({'message': 'you are like this'}, status=status.HTTP_200_OK)


class LikeListApiViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikeListSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FollowUnfollowViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk, format=None):
        current_page = get_object_or_404(Page, owner=self.request.user)
        other_page = get_object_or_404(Page, id=pk)
        if other_page.is_private:
            other_page.follow_requests.add(current_page)
            return Response({"Requested": "Follow request has been send!!"}, status=status.HTTP_200_OK)
        else:
            current_page.following.add(other_page)
            other_page.followers.add(current_page)
            return Response({"Following": "Following success!!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk, format=None):
        current_page = get_object_or_404(Page, owner=self.request.user)
        other_page = get_object_or_404(Page, id=pk)
        current_page.follow_requests.remove(other_page)
        return Response({"Accepted": "Follow request successfuly accespted!!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk, format=None):
        current_page = get_object_or_404(Page, owner=self.request.user)
        other_page = get_object_or_404(Page, id=pk)
        current_page.follow_requests.remove(other_page)
        return Response({"Decline": "Follow request successfully declined!!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk, format=None):
        current_page = get_object_or_404(Page, owner=self.request.user)
        other_page = get_object_or_404(Page, id=pk)
        other_page.followers.remove(current_page)
        return Response({"Unfollow": "Unfollow success!!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove(self, request, pk, format=None):
        current_page = get_object_or_404(Page, owner=self.request.user)
        other_page = get_object_or_404(Page, id=pk)
        current_page.followers.remove(other_page)
        other_page.following.remove(current_page)
        return Response({"Remove Success": "Successfuly removed your follower!!"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def follow_detail(self, request, format=None):

        current_page = get_object_or_404(Page, owner=self.request.user)
        serializer = FollowerSerializer(current_page)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class NewsView(viewsets.ViewSet):

    def list(self, request):
        followers = self.request.user.pages.first().followers.all()
        follower_posts = []
        for follower in followers:
            for follower_post in follower.posts.all():
                follower_posts.append(follower_post)
        serializer = PostSerializer(follower_posts, many=True)
        return Response(serializer.data)
