from authentication.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Page, Post, Reply, Tag


# class FilterAnswerListSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         data = data.filter(parent=None)
#         return super().to_representation(data)
#
#
# class RecursiveSerializer(serializers.Serializer):
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data


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


class ReplySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        # list_serializer_class = FilterAnswerListSerializer
        model = Reply
        fields = ('owner', 'reply_text')


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.ReadOnlyField(source='page.name')
    replies = ReplySerializer(many=True, read_only=True)
    like = serializers.SlugRelatedField(
        many=True, slug_field='username', queryset=User.objects.all())

    # like = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'owner', 'page', 'content', 'replies', 'like', 'created_at', 'updated_at')
        # fields = '__all__'

    # def update(self, instance, validated_data):
    #     liked = validated_data.pop('like')
    #     for i in liked:
    #         instance.liked.add(i)
    #     instance.save()
    #     return instance


class PostLikeListSerializer(serializers.ModelSerializer):
    likes = PostSerializer(many=True, read_only=True)  # likes is in Post model with foreign key to user Model

    class Meta:
        model = Post
        fields = ['like', ]
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
