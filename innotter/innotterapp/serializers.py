from rest_framework import serializers

from .models import Page, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = TagSerializer(read_only=True, many=True)
    # followers = FollowersSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('owner', 'uuid', 'description', 'tags', 'followers', 'image', 'follow_requests',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
