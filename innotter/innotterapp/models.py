import uuid

from authentication.models import User
# from content_interaction.models import Like
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models


class Name(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Tag(Name):
    pass


class Page(Name):
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='pages')
    uuid = models.CharField(max_length=32, unique=True, default=uuid.uuid4().hex)
    description = models.TextField()
    tags = models.ManyToManyField('innotterapp.Tag', related_name='pages', blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    #####################
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
    follow_requests = models.ManyToManyField('self', blank=True, related_name='followRequest', symmetrical=False)
    created_date = models.DateTimeField(auto_now_add=True)
    ######################
    unblock_date = models.DateTimeField(null=True, blank=True)
    # followers = models.ManyToManyField(
    #     'authentication.User',
    #     null=True, blank=True,
    #     related_name='follows'
    # )
    # follow_requests = models.ManyToManyField(
    #     'authentication.User',
    #     null=True, blank=True,
    #     related_name='requests'
    # )


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField('authentication.User', blank=True, related_name='likes', symmetrical=False)

    # likes = GenericRelation(Like)
    # reply_to = models.ForeignKey('innotterapp.Post', on_delete=models.SET_NULL, null=True, related_name='replies')


class Reply(models.Model):
    owner = models.ForeignKey('authentication.User', related_name='replies', on_delete=models.CASCADE)
    reply_text = models.TextField(max_length=255)
    parent = models.ForeignKey(
        'self', verbose_name="parent", on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )
    posts = models.ForeignKey(Post, verbose_name="post", on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return self.reply_text

# class Reply(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     owner = models.ForeignKey('authentication.User', related_name='replies', on_delete=models.CASCADE)
#     reply_text = models.TextField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
#
#     class Meta:
#         ordering = ('-created_at',)
#
#     def __str__(self):
#         return f'Comment by {self.owner.username} on {self.post}'
#
#     def children(self):
#         return Reply.objects.filter(parent=self)
#
#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True
