import uuid

from django.contrib.auth import get_user_model
from rest_framework import serializers

from mainapp.models import Page, Post, Reply, Tag

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class EachPageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='page.name')

    class Meta:
        model = Page
        fields = ('id', 'name', 'owner')
        read_only_fields = ('id', 'name', 'owner')


class FollowerSerializer(serializers.ModelSerializer):
    followers = EachPageSerializer(many=True, read_only=True)
    following = EachPageSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ('followers', 'following')
        read_only_fields = ('followers', 'following')


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    uuid = serializers.UUIDField(default=uuid.uuid4().hex)
    tags = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Tag.objects.all())
    followers = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=User.objects.all())
    following = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=User.objects.all())

    class Meta:
        model = Page
        exclude = ('unblock_date', 'created_date')

    def to_internal_value(self, data):
        for tag_name in data.get('tags', []):
            Tag.objects.get_or_create(name=tag_name)
        return super().to_internal_value(data)


class FilterAnswerListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReplySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Reply
        fields = ('owner', 'reply_text', 'posts')


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.ReadOnlyField(source='page.name')
    replies = ReplySerializer(many=True, read_only=True)
    like = serializers.SlugRelatedField(
        many=True, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'owner', 'page', 'content', 'replies', 'like')


class PostLikeListSerializer(serializers.ModelSerializer):
    likes = PostSerializer(many=True, read_only=True)  # likes is in Post model with foreign key to user Model

    class Meta:
        model = Post
        fields = ['like', ]



