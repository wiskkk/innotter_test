from rest_framework import serializers

# from innotterapp.models import Page
# from .models import PageFollowing


# class PageSerializer(serializers.ModelSerializer):
#     following = serializers.SerializerMethodField()
#     followers = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Page
#         fields = (
#             "id",
#             "name",
#             "owner",
#             "following",
#             "followers",
#         )
#
#     def get_following(self, obj):
#         return FollowingSerializer(obj.following.all(), many=True).data
#
#     def get_followers(self, obj):
#         return FollowersSerializer(obj.followers.all(), many=True).data

#
# class FollowingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PageFollowing
#         fields = ("id", "following_page_id", "created")
#
#
# class FollowersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PageFollowing
#         fields = ("id", "page_id", "created")
