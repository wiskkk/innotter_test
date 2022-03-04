from django.core import exceptions
from rest_framework import serializers
from .models import Page, Post, Tag
from authentication.models import User


class TagsField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    tags = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Tag.objects.all())

    # tags = TagsSerializer(read_only=True, many=True)
    # tags = TagsField(source="get_tags")
    # followers = serializers.StringRelatedField(many=True)

    # def create(self, validated_data):
    #     tags = validated_data.pop("get_tags")
    #     page = Page.objects.create(**validated_data)
    #     page.tags.add(*tags)
    #
    #     return page

    class Meta:
        model = Page
        exclude = ('unblock_date',)
        # fields = ('id', 'name', 'owner', 'owner_email', 'uuid', 'description', 'tags', 'image', 'is_private')

    def to_internal_value(self, data):
        for tag_name in data.get('tags', []):
            Tag.objects.get_or_create(name=tag_name)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
