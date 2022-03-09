from authentication.models import User
from rest_framework import serializers

from .models import Page, Post, Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    tags = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Tag.objects.all())
    followers = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=User.objects.all())
    following = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=User.objects.all())

    class Meta:
        model = Page
        exclude = ('unblock_date', 'follow_requests')

    def to_internal_value(self, data):
        for tag_name in data.get('tags', []):
            Tag.objects.get_or_create(name=tag_name)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    page = serializers.ReadOnlyField(source='page.name')

    class Meta:
        model = Post
        fields = '__all__'


# class EachUserSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='user.name')
#
#     class Meta:
#         model = Page
#         fields = ('id', 'name')
#         read_only_fields = ('id', 'name')
#
#
# class FollowerSerializer(serializers.ModelSerializer):
#     followers = EachUserSerializer(many=True, read_only=True)
#     following = EachUserSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Page
#         fields = ('followers', 'following')
#         read_only_fields = ('followers', 'following')
