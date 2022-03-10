from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Page, Post, Reply, Tag
from .serializers import PageSerializer, PostLikeListSerializer  # FollowerSerializer,
from .serializers import PostSerializer, ReplySerializer, TagsSerializer


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


class PostViewSet(PermissionMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(page=self.request.user.pages.first())

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RepliesViewSet(PermissionMixin):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class FollowView(viewsets.ViewSet):
    queryset = Page.objects

    def follow(self, request, pk):
        own_page = request.user.pages.first()  # or your queryset to get
        following_page = Page.objects.get(id=pk)
        own_page.following.add(following_page)  # and .remove() for unfollow
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        # your unfollow code
        return Response({'message': 'you are no longer following him'}, status=status.HTTP_200_OK)


# class LikeUnlikeView(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def post(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         if post.like.filter(pk=request.user.pk).exists():
#             post.like.remove(request.user)
#         else:
#             post.like.add(request.user)
#         return Response({'message': 'you are like this'}, status=status.HTTP_200_OK)

class LikeUnlikeViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(like__username=self.request.user.username)
        return queryset

    @action(detail=True, methods=['post'])
    def liked(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.like.filter(pk=request.user.pk).exists():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        return Response({'message': 'you are like this'}, status=status.HTTP_200_OK)


class LikeListApiView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikeListSerializer
    permission_classes = (permissions.IsAuthenticated,)

# class FollowUnfollowView(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def current_page(self):
#         try:
#             return Page.objects.get(owner=self.request.user)
#         except Page.DoesNotExist:
#             raise Http404
#
#     def other_page(self, pk):
#         try:
#             print(Page.objects.get(id=self.request.data.id))
#             return Page.objects.get(id=pk)
#         except Page.DoesNotExist:
#             raise Http404
#
#     def post(self, request, format=None):
#         print(request.data)
#         pk = request.data.get('id')  # Here pk is opposite user's profile ID
#         req_type = request.data.get('type')
#         current_page = self.current_page()
#         other_page = self.other_page(pk)
#         if req_type == 'follow':
#             if other_page.private_account:
#                 other_page.panding_request.add(current_page)
#                 return Response({"Requested": "Follow request has been send!!"}, status=status.HTTP_200_OK)
#             else:
#                 current_page.following.add(other_page)
#                 other_page.followers.add(current_page)
#                 return Response({"Following": "Following success!!"}, status=status.HTTP_200_OK)
#
#         elif req_type == 'accept':
#             current_page.followers.add(other_page)
#             other_page.following.add(current_page)
#             current_page.panding_request.remove(other_page)
#             return Response({"Accepted": "Follow request successfuly accespted!!"}, status=status.HTTP_200_OK)
#
#         elif req_type == 'decline':
#             current_page.panding_request.remove(other_page)
#             return Response({"Decline": "Follow request successfully declined!!"}, status=status.HTTP_200_OK)
#
#         elif req_type == 'unfollow':
#             current_page.following.remove(other_page)
#             other_page.followers.remove(current_page)
#             return Response({"Unfollow": "Unfollow success!!"}, status=status.HTTP_200_OK)
#
#         elif req_type == 'remove':  # You can remove your follower
#             current_page.followers.remove(other_page)
#             other_page.following.remove(current_page)
#             return Response({"Remove Success": "Successfuly removed your follower!!"}, status=status.HTTP_200_OK)
#
#     # Here we can fetch followers,following detail and blocked user,pending request,sended request..
#
#     def patch(self, request, format=None):
#
#         req_type = request.data.get('type')
#
#         if req_type == 'follow_detail':
#             serializer = FollowerSerializer(self.current_page())
#             return Response({"data": serializer.data}, status=status.HTTP_200_OK)
